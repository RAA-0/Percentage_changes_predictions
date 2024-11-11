from selenium import webdriver 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from collections import defaultdict
from abstract_scraper import AbstractScraper
import json 
import time
import random 

class SportsScraper(AbstractScraper):
    def __init__(self):
       super().__init__()

    @property
    def website_url(self):
        return ["https://www.scoreandchange.com/sports_events/past-events","https://www.scoreandchange.com/sports_events/"]

    def get_url(self,url):
        driver = super().get_url(url)
        try:
            accept_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "cky-btn-accept"))
            )
            accept_button.click()
        except Exception as e:
            print("No cookie consent pop-up found or couldn't click the button:", e)
        time.sleep(random.uniform(2,5))
        return driver 

    
    def scrape_news(self):
        news=[]
        year_lists = defaultdict(lambda:defaultdict(defaultdict))
        urls = self.website_url
        for url in urls: 
            driver = self.get_url(url)
            lists = driver.find_elements(By.TAG_NAME,"p")
            
            for list in lists:
                news.append(list.text)
            
            news = [event for event in news if ("|" in event)&("Jump to" not in event)]        
        
            with open("Scraping\\Sports_\\sportsnews.json","w") as w:
                json.dump(news,w,indent=4)

    def run(self):
        self.scrape_news()

if __name__ == "__main__":
    scraper = SportsScraper()
    scraper.run()