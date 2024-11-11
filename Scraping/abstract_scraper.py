from selenium import webdriver
from selenium.webdriver import chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
import time
import random

class AbstractScraper:
    def __init__(self):
        pass 
    @property
    def website_url(self):
        return ''
    
    def get_url(self,url):
        service = Service(executable_path="C:/Users/Lenovo/Desktp/chromedriver-win64/chromedriver.exe")
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(service = service)
        driver.get(url)
        time.sleep(random.uniform(2,5))
        return driver
    def scrape_news(self):
        return {}
    def run(self):
        return 
    

