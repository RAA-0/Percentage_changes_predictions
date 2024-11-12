from selenium import webdriver
from selenium.webdriver import chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
import time
import random
import json

class AbstractScraper:
    def __init__(self,event):
        self.event = event
        self.config=self.read_config()
        self.data=self.read_file(self.file_path)
        self.mapping ={"Jan":"01","Feb":"02", "Mar":"03","Apr":"04","May":"05","Jun":"06","Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"}

        
    @property 
    def file_path(self):
        return self.config[self.event]['file_path']

    @property
    def website_url(self):
        return self.config[self.event]['website']
    
    @property
    def df_path(self):
        return self.config[self.event]['df_path']

    
    def get_url(self,url):
        service = Service(executable_path="C:/Users/Lenovo/Desktp/chromedriver-win64/chromedriver.exe")
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(service = service)
        driver.get(url)
        time.sleep(random.uniform(2,5))
        return driver

    def run(self):
        return 

    def scrape_news(self):
        return {}

    def fix_form(self):
        return 
    def merge_and_save(self):
        pass

    def detect_event(self,date):
        return []
    
    def read_file(self,file_path):
        with open(file_path) as jsonreader:
            return json.load(jsonreader)
    def read_config(self):
        with open('Scraping\\config.json') as f:
            return json.load(f)
    

