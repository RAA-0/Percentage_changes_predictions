
from datetime import date
import pandas as pd 
import json
from Scraping.Global_health.GlobalHealthScraper import GlobalHealthScraper
from Scraping.Global_health.ExtractingGlobalHealthFeature import GlobalHealthExtractor

def main(date):
    events =[]
    with open("Scraping\\Global_health\\GlobalHealthNews.json") as f:
        scraped_news = json.load(f)
    df = pd.read_csv('Scraping\\Global_health\\globalCrisisFeature.csv')

    date = pd.to_datetime(date)
    year = date.year
    month = date.month
    day = date.day
    
    matching_rows = df[(pd.to_datetime(df['month_end']).dt.year == year) & (pd.to_datetime(df['month_end']).dt.month == month)]
    
    if not matching_rows.empty:
        health_crisis = matching_rows.iloc[0]['health_crisis_month']
    else:
        return 0
        scraper = GlobalHealthScraper([year])
        new_news = scraper.run()
        if year in scraped_news and month in scraped_news[year] and day in scraped_news[year][month]:
            ghe = GlobalHealthExtractor
            ghe.run()
            new_df = pd.read_csv('Scraping\\Global_health\\globalCrisisFeature.csv')
            matching_rows = new_df[(pd.to_datetime(new_df['month_end']).dt.year == year) & (pd.to_datetime(new_df['month_end']).dt.month == month)]
            if matching_rows.empty:
                #there was no news in this month 
                health_crisis=0
            else:
                health_crisis = matching_rows.iloc[0]['health_crisis_month']

    return health_crisis 

if __name__=='__main__':
    main('2022-11-24')



