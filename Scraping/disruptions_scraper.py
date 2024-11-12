from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import defaultdict
from Scraping.abstract_scraper import AbstractScraper
import json 
import time
import random 
import pandas as pd 


class DisruptionsScraper(AbstractScraper):
    def __init__(self):
        super().__init__("disruptions")

    def run(self):
        news = self.scrape_news()
        with open(self.file_path,"w") as jw:
            json.dump(news,jw,indent=4)
        self.fix_form(news)

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
            driver = self.get_url(self.website_url.format(s=self.s))
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
    
    def fix_form(self,data):
        new_df = pd.DataFrame()
        for date , news in data.items():
                df = pd.DataFrame({'year':[date.split("\n")[2]],'month':[self.mapping[date.split("\n")[1]]],'day':[date.split("\n")[0]],'news':[news_headline for news_headline in news.keys()]})
                new_df=pd.concat([new_df,df])

        new_df.to_csv(self.df_path,index=False)
    def detect_event(self,date):
        events=[]
        keywords =['disruption due to weather','weather disruption']
        df = pd.read_csv(self.df_path)
        df['date'] = pd.to_datetime(df[['year', 'month','day']])
        matching_rows = df[pd.to_datetime(df['date'])==pd.to_datetime(date)]
        if not matching_rows.empty:
            news = matching_rows.iloc[0]['news']
            for i in keywords:
                if i in news:
                    events.append('disruption')
        return events 


if __name__=="__main__":
    ds = DisruptionsScraper()
    ds.run()


