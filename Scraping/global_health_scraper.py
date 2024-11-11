from selenium import webdriver 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from collections import defaultdict
from abstract_scraper import AbstractScraper
from selenium.webdriver.common.action_chains import ActionChains
import json 
import time
import random 


class GlobalHealthScraper(AbstractScraper):
    def __init__(self,years):
        super().__init__()
        self.years = years
        self.years_indices()

    @property
    def website_url(self):
        return "https://www.who.int/news"
    
    
    def scrape_news(self,n):
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
            print("hon numbber pf page",pages)
            page =1
            try:
                while page<=int(pages):
                    print(f"page:{page}")
                    main = driver.find_element(By.CLASS_NAME,"hubfiltering").find_element(By.CLASS_NAME,"k-listview-content")
                    news = main.find_elements(By.TAG_NAME,"p")
                    time_stamp = main.find_elements(By.TAG_NAME, "span")
                    for date,news in zip(time_stamp,news):
                        if date.text in n:
                            n[date.text].append(news.text)
                        else:
                            n[date.text] = [news.text]
                        self.new_news[date.text].append(news.text)
                        
                    print(n)
                    
                    print(f"finished page {page} of {pages} ")
                    page+=1              
                
                    page_input = driver.find_element(By.XPATH,'/html/body/div[3]/section/div[2]/div/div/div/div[2]/div[2]/div/div[2]/div[2]/span[1]/input')
                    # Change the page to 2
                    page_input.clear()  # Clear the input field first
                    page_input.send_keys(str(page))  # Enter the page number
                    page_input.send_keys(Keys.ENTER)  # Simulate pressing Enter

                    # Wait for the input field to update to "2"
                    WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((By.XPATH, f"/html/body/div[3]/section/div[2]/div/div/div/div[2]/div[2]/div/div[2]/div[2]/span[1]/input[@aria-label='{page}']"))
                    )                 
                    print(n)
                    with open("GlobalHealthNews2022.json","w") as ww:
                        json.dump(n,ww,indent=4)
            except:
                print("there was a problem")
                with open("AUXGlobalHealthNews2w.json","w") as w2w:
                        json.dump(n,w2w,indent=4)
            

    def run(self):
        with open("Scraping\\Global_health\\AUXGlobalHealthNews2.json","r") as w:
            old_data = json.load(w)
        self.scrape_news(old_data)
        return self.new_news
    
    def years_indices(self,start_year=None):
        self.index_of_year=defaultdict(str)
        if start_year is None:
            start_year = 2025
        for i in range(0,36):
            self.index_of_year[str(start_year)]=str(i)
            start_year-=1 

if __name__ == "__main__":
    scraper = GlobalHealthScraper(["2024"])
    scraper.run()
