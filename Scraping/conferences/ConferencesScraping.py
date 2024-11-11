from selenium import webdriver 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import time 
import random 
from collections import defaultdict
import json 

class ConferenceScraping:
    def __init__(self):
        pass
    def get_url(self,url):
        service = Service(executable_path="C:/Users/Lenovo/Desktp/chromedriver-win64/chromedriver.exe")
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(service = service)
        driver.get(url)
        time.sleep(random.uniform(2,5))
        return driver         
    def scrape_news(self, date):
        news=defaultdict(lambda: defaultdict(list))
        dates = []
        url = 'https://www.allconferencealert.com/dubai.html'
        driver =self.get_url(url)
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

                    with open('Scraping\\conferences\\n2.json','w') as fe:
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
            

    def merge_and_save(self,old,new):
        for year in new.keys():
            if not year in old.keys():
                old.update(new)
            else:
                for date in new[year].keys():
                    if not date in old[year].keys():
                        old[year][date]=new[year][date]
                    else:
                        old[year][date].append(new[year][date])
        for outer_key, inner_dict in old.items():
            for inner_key, value_list in inner_dict.items():
                inner_dict[inner_key] = list(set(value_list))
        with open('Scraping\\conferences\\conference_news.json','w') as fw :
            json.dump(old,fw,indent=4)
            

            

    def run (self,date):
        with open('Scraping\\conferences\\conference_news.json','r') as fr:
            old_data = json.load(fr)
        new_data = self.scrape_news(date)
        if new_data is not None and bool(new_data):
            self.merge_and_save(old_data,new_data)
        else:
            print("there are no news for this date")


        


            
        

cs=ConferenceScraping()
cs.run("All")

