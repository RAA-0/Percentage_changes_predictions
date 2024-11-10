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


class DisruptionsScraper:
    def __init__(self):
        pass

    def get_url(self,url):
        service = Service(executable_path="C:/Users/Lenovo/Desktp/chromedriver-win64/chromedriver.exe")
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(service = service)
        driver.get(url)
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
        s = 0
        done = False
        while not done:
            newss = defaultdict(lambda: defaultdict(dict))
            url = f"https://media.dubaiairports.ae/?s={s}&q=disruption+"
            driver = self.get_url(url)
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
            s+=10

        return news
    def run(self):
        news = self.scrape_news()
        with open('Scraping\\Disruptions\\nn.json',"w") as jw:
            json.dump(news,jw,indent=4)

if __name__=="__main__":
    ds = DisruptionsScraper()
    ds.run()


