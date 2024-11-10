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


class GlobalHealthScraper:
    def __init__(self,years):
        self.years = years

    def get_url(self,url):
        service = Service(executable_path="C:/Users/Lenovo/Desktp/chromedriver-win64/chromedriver.exe")
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(service = service)
        driver.get(url)
        time.sleep(random.uniform(2,5))
        return driver 
    
    
    def scrape_news(self,n):
        url = "https://www.who.int/news"
        driver = self.get_url(url)
        self.new_news=defaultdict
        for year in self.years:
            try:
                print("still waiting...")
                year_dropdown = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/section/div[2]/div/div/div/div[2]/div[2]/div/div[1]/div/div/div/div[5]/span/span')))
                driver.execute_script("arguments[0].click();",year_dropdown)
                #year_dropdown.click()
                year_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//li[@data-offset-index='4']")))
                year_option.click()
                print(f"year  is clicked")
                
            except:
                print("the year was not chosen")
                return None
            #timestamp_element = WebDriverWait(driver, 10).until( EC.text_to_be_present_in_element((By.XPATH, '//*[@id="listView-8ab62796-d0cf-4165-9188-c369f555a2b6"]/div/div[1]/a/div[2]/div/span'), "2020"))
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
                        self.new_news.append(news.text)
                        
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
                with open("AUXGlobalHealthNews2.json","w") as w2w:
                        json.dump(n,w2w,indent=4)
            

    def run(self):
        with open("Scraping\\Global_health\\AUXGlobalHealthNews2.json","r") as w:
            old_data = json.load(w)
        self.scrape_news(old_data)
        return self.new_news

if __name__ == "__main__":
    scraper = GlobalHealthScraper(["2024"])
    scraper.run()
