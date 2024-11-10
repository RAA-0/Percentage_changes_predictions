from datetime import date
import pandas as pd 
import json
from Scraping.Sports_.ScrapingMajorSportsNews import MajorSportsNewsScraper
import ast

def get_event(df,date):
        year = date.year
        month = date.month
        day = date.day
        matching_rows = df[ (df['year'].astype(int) == int(year)) & (df['month'].astype(int)== month)]
        events_on_day = []
        for _, row in matching_rows.iterrows():
            if isinstance(row['days'], str) and row['days'].startswith('['):
                day_list = ast.literal_eval(row['days'])
                if day in day_list:
                    if "FIFA World Cup" in row['event'] and "football men" in row['event']:
                        row['event']='world_cup'
                        events_on_day.append(row['event'])
                elif row['days'] == day:
                    events_on_day.append(row['event'])    
        return events_on_day 

def main(date):
    df = pd.read_csv('Scraping\\Sports_\\sports_df.csv')
    df['date'] = pd.to_datetime(df[['year', 'month']].assign(day=1))
    max_date = df['date'].max()
    date = pd.to_datetime(date)
    if date<=max_date:
        events_on_day = get_event(df,date)
        print(events_on_day)
    else:
        return []
        sns= MajorSportsNewsScraper()
        sns.run()
        events_on_day = get_event(df,date)
    return events_on_day





