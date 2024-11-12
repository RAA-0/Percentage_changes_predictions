from datetime import date
import pandas as pd 
import json
from ScrapingMajorSportsNews import MajorSportsNewsScraper
import ast

def get_event(df,date):
        year = date.year
        month = date.month
        day = date.day
        matching_rows = df[ (df['year'].astype(int) == int(year)) & (df['month'].astype(int)== month)&(df['day'].astype(int)==day)]
        events_on_day = []
        for _, row in matching_rows.iterrows():
            events_on_day.append(row['event'])    
        return events_on_day 

def main(date):
    df = pd.read_csv('Scraping\\Sports_\\expanded_sports_df.csv')
    df['date'] = pd.to_datetime(df[['year', 'month','day']])
    max_date = df['date'].max()
    date = pd.to_datetime(date)
    if date<=max_date:
        events_on_day = get_event(df,date)
        print(events_on_day)
    else:
        sns= MajorSportsNewsScraper()
        sns.run()
        events_on_day = get_event(df,date)
    return events_on_day
main('2025-1-6')




