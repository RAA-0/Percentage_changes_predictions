from selenium import webdriver 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from collections import defaultdict
import json 
import time
import random 


class MajorSportsNewsScraper:
    def __init__(self):
       pass

    def get_url(self,url):
        service = Service(executable_path="C:/Program Files (x86)/chromedriver.exe")
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(service = service)
        driver.get(url)
        time.sleep(random.uniform(2,5))
        return driver 
    #/html/body/div[5]/div/div/div/div/main/div[2]/article/div/h1[1]
    #/html/body/div[5]/div/div/div/div/main/div[2]/article/div/h1[9]
    #/html/body/div[5]/div/div/div/div/main/div[2]/article/div/h1[43]
    
    
    def scrape_news(self,old_data):
        year = '2022'
        news=[]
        year_lists = defaultdict(lambda:defaultdict(defaultdict))
        url = f"https://www.scoreandchange.com/sports_events/past-events/#{year}"
        driver = self.get_url(url)
        year = driver.find_element(By.XPATH,'/html/body/div[5]/div/div/div/div/main/div[2]/article/div/h1[22]').text
        print(year)
        lists = driver.find_elements(By.TAG_NAME,"p")
        
        for list in lists:
            news.append(list.text)
    
        with open("Sports Major Events\\sportsnews.json","w") as w:
            json.dump(news,w,indent=4)

    def run(self):
        with open("Sports Major Events\\sportsnews.json","r") as w:
            old_data = json.load(w)
        
        self.scrape_news(old_data)

if __name__ == "__main__":
    scraper = MajorSportsNewsScraper()
    scraper.run()