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


class DisruptionsScraper(AbstractScraper):
    def __init__(self):
        super().__init__()

    @property
    def website_url(self):
        return f"https://media.dubaiairports.ae/?s={self.s}&q=disruption+"


    def get_url(self,url):
        driver = super().get_url(url)
        try:
            accept_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/a[2]'))
            )
            accept_button.click()
        except Exception as e:
            print("No cookie consent pop-up found or couldn't click the button:", e)
        
        time.sleep(random.uniform(2,5))
        return driver 
    def scrape_news(self):
        news=defaultdict(lambda: defaultdict(dict))
        self.s = 0
        done = False
        while not done:
            newss = defaultdict(lambda: defaultdict(dict))
            driver = self.get_url(self.website_url)
            table_cntent=driver.find_element(By.TAG_NAME,"tbody")
            tds = table_cntent.find_elements(By.CLASS_NAME,"td_content")
            for td in tds:
                date = td.find_element(By.CLASS_NAME,"searchresult_title").text
                headline_link =td.find_element(By.TAG_NAME,"a")
                link= headline_link.get_attribute("href")
                headline= headline_link.text
                newss[date]={headline:link}
            if not newss:
                done =True
            else:
                news.update(newss)
            self.s+=10

        return news
    def run(self):
        news = self.scrape_news()
        with open('Scraping\\Disruptions\\nn3.json',"w") as jw:
            json.dump(news,jw,indent=4)

if __name__=="__main__":
    ds = DisruptionsScraper()
    ds.run()


