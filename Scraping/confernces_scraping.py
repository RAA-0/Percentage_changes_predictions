from selenium import webdriver 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from Scraping.abstract_scraper import AbstractScraper
import time 
import random 
from collections import defaultdict
import json 
import pandas as pd
import ast 

class ConferenceScraper(AbstractScraper):
    def __init__(self):
        super().__init__("conferences")
         
    def run (self,date):
        new_data = self.scrape_news(date)
        if new_data is not None and bool(new_data):
            self.merge_and_save(new_data)
        else:
            print("there are no news for this date")
        self.fix_form()

    def scrape_news(self, date):
        news=defaultdict(lambda: defaultdict(list))
        dates = []
        driver =super().get_url(self.website_url)
        month_year_elem = driver.find_element(By.XPATH,'/html/body/div[3]/div[1]/div[2]/div/div/div[1]/ul')
        month_year_elements = month_year_elem.find_elements(By.TAG_NAME,"li")
        found = False
        if date != "All":
            year = date.split(" ")[1]
        else:
            dates = [month_year_element1.text for month_year_element1 in month_year_elements]
        for month_year_element in month_year_elements:
            if date in month_year_element.text:
                ActionChains(driver).move_to_element(month_year_element).click().perform()
                time.sleep(random.uniform(2, 5)) 
                print(f"Scraping conferences for {date}...")
                found = True
                break
            
        if not found:
            print(f"Date {date} not found in the options.")
            driver.quit()
            return 
        while True:
            try:    
                table = driver.find_element(By.TAG_NAME,'tbody')
                data = table.find_elements(By.CLASS_NAME,'data1')
                for td in data:
                    print("scraping..")
                    date_conference =  td.find_elements(By.TAG_NAME,'a')
                    if not dates:
                        news[year][date_conference[0].text].append(date_conference[1].text)
                    else:
                        month = date_conference[0].text.split(" ")[1]
                        for date in dates:
                            if month in date:
                                year = date.split(" ")[1]
                                break
                        news[year][date_conference[0].text].append(date_conference[1].text)

                    with open(self.file_path,'w') as fe:
                        json.dump(news,fe,indent=4)
                try:
                    next_button = driver.find_element(By.XPATH, "//li[@class='active' and text()='Next']")
                    ActionChains(driver).move_to_element(next_button).click().perform()
                    time.sleep(10)
                    print("next page")
                except:
                    print("Reached the last page.")
                    return news
            except Exception as e:
                print(f"AN error occured due to : {e}")
                return news
            

    def merge_and_save(self,new):
        for year in new.keys():
            if not year in self.data.keys():
                self.data.update(new)
            else:
                for date in new[year].keys():
                    if not date in self.data[year].keys():
                        self.data[year][date]=new[year][date]
                    else:
                        self.data[year][date].extend(new[year][date])
        for year, inner_dict in self.data.items():
            for date, conferences in inner_dict.items():
                inner_dict[date] = list(set(conferences))
        with open(self.file_path,'w') as fw :
            json.dump(self.data,fw,indent=4)

    def fix_form(self):
        new_df = pd.DataFrame()
        for year in  self.data.keys():
            for date , list in self.data[year].items():
                ddf = pd.DataFrame({'year':[year],'month':[self.mapping[date.split(" ")[1]]],'day':[date.split(" ")[0]],'conferences':[list]})
                new_df=pd.concat([new_df,ddf])
        new_df.to_csv(self.df_path,index=False)

    def detect_event(self,date_input):
        events =[]
        with open(self.file_path) as f:
            scraped_news = json.load(f)
        df = pd.read_csv(self.df_path)

        date_input = pd.to_datetime(date_input)
        year = date_input.year
        month = date_input.month
        day = date_input.day
        
        matching_rows = df[(df['year'].astype(int) == year) & (df['month'].astype(int)== month) & (df['day'].astype(int)== day) ]
        
        if not matching_rows.empty:
            conference_event = matching_rows.iloc[0]['conferences']
            conference_event = ast.literal_eval(conference_event)  
            if any(word in conference_event for word in self.config[self.event]['impactful_event']):
                events.extend(conference_event)
        return events

