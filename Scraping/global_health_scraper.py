from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from collections import defaultdict
from Scraping.abstract_scraper import AbstractScraper
from selenium.webdriver.common.action_chains import ActionChains
from Scraping.Global_health.ExtractingGlobalHealthFeature import GlobalHealthExtractor
import json 
import pandas as pd 
from datetime import datetime

class GlobalHealthScraper(AbstractScraper):
    def __init__(self,years=None):
        super().__init__("global_health")
        self.years = years
        self.years_indices()
    
    def run(self):
        self.scrape_news()
        #self.fix_form()
 
    def scrape_news(self):
        driver = super().get_url(self.website_url)
        self.new_news=defaultdict(list)
        for year in self.years:
            try:
                print("still waiting...")
                year_dropdown = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/section/div[2]/div/div/div/div[2]/div[2]/div/div[1]/div/div/div/div[5]/span/span/span[2]/span')))
                ActionChains(driver).move_to_element(year_dropdown).click().perform()
                year_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//li[@data-offset-index='{self.index_of_year[year]}']")))
                year_option.click()
                print(f"year {year}  is clicked")
                
            except:
                print("the year was not chosen")
                return None
            WebDriverWait(driver, 20).until(
        lambda driver: year in driver.find_element(By.CLASS_NAME, "hubfiltering")
                                .find_element(By.CLASS_NAME, "k-listview-content")
                                .find_element(By.TAG_NAME, "span").text
    )
            print("searching for the news")
            pages = driver.find_element(By.ID,'ppager').find_element(By.CLASS_NAME, "k-pager-last").get_attribute("data-page") 
            print("number of page",pages)
            page =1
            try:
                while page<=int(pages):
                    print(f"page:{page}")
                    main = driver.find_element(By.CLASS_NAME,"hubfiltering").find_element(By.CLASS_NAME,"k-listview-content")
                    news = main.find_elements(By.TAG_NAME,"p")
                    time_stamp = main.find_elements(By.TAG_NAME, "span")
                    for date,news in zip(time_stamp,news):
                        if date.text in self.data:
                            self.data[date.text].append(news.text)
                        else:
                            self.data[date.text] = [news.text]
                        self.new_news[date.text].append(news.text)
                        
                    print(self.data)
                    
                    print(f"finished page {page} of {pages} ")
                    page+=1              
                
                    page_input = driver.find_element(By.XPATH,'/html/body/div[3]/section/div[2]/div/div/div/div[2]/div[2]/div/div[2]/div[2]/span[1]/input')
                    page_input.clear()  
                    page_input.send_keys(str(page)) 
                    page_input.send_keys(Keys.ENTER)

                    WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((By.XPATH, f"/html/body/div[3]/section/div[2]/div/div/div/div[2]/div[2]/div/div[2]/div[2]/span[1]/input[@aria-label='{page}']"))
                    )                 
                    print(self.data)
                    with open(self.file_path,"w") as ww:
                        json.dump(self.data,ww,indent=4)
            except:
                print("there was a problem")
                with open("AUXGlobalHealthNews2w.json","w") as w2w:
                        json.dump(self.data,w2w,indent=4)
    
    def fix_form(self):
        ghe = GlobalHealthExtractor(self.data,self.config['global_health']['aux_df'],self.config['keywords'],self.df_path)
        ghe.run()
    
    def detect_event(self,date_input):
        events =[]
        with open(self.file_path) as f:
            scraped_news = json.load(f)
        df = pd.read_csv(self.df_path)

        date_input = pd.to_datetime(date_input)
        year = date_input.year
        month = date_input.month
        day = date_input.day
        
        matching_rows = df[(pd.to_datetime(df['month_end']).dt.year == year) & (pd.to_datetime(df['month_end']).dt.month == month)]
        
        if not matching_rows.empty:
            health_crisis = matching_rows.iloc[0]['health_crisis_month']
        else:
            if date_input < datetime.now() or ((date_input.year == datetime.now().year) and (date_input.month== datetime.now().month)):
                scraper = GlobalHealthScraper([year])
                new_news = scraper.run()
                if year in scraped_news and month in scraped_news[year] and day in scraped_news[year][month]:
                    ghe = GlobalHealthExtractor
                    ghe.run()
                    new_df = pd.read_csv('Scraping\\Global_health\\globalCrisisFeature.csv')
                    matching_rows = new_df[(pd.to_datetime(new_df['month_end']).dt.year == year) & (pd.to_datetime(new_df['month_end']).dt.month == month)]
                    if matching_rows.empty:
                        health_crisis=0
                    else:
                        health_crisis = matching_rows.iloc[0]['health_crisis_month']
            else: return []

        return ['corona'] if health_crisis==1 else []

    def years_indices(self,start_year=None):
        self.index_of_year=defaultdict(str)
        if start_year is None:
            start_year = 2025
        for i in range(0,36):
            self.index_of_year[str(start_year)]=str(i)
            start_year-=1 
    
