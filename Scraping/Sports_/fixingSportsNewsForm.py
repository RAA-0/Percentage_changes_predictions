import pandas as pd
import re 
import json 
import ast

class FormFixer:
    def __init__(self,file_path,df_path):
        self.file_path = file_path
        self.df_path = df_path
        self.mapping ={"January":"01","February":"02", "March":"03","April":"04","May":"05","June":"06","July":"07","August":"08","September":"09","October":"10","November":"11","December":"12"}

    def extract_date(self,date):   
        pattern0 = re.compile(r'(\d{1,2})(\D+)(\d{4})[-\u2013](\d{1,2})(\D+)(\d{4})')##28December2023–7January2024
        pattern1 = re.compile(r'(\d{1,2})(\D+)[-\u2013](\d{1,2})(\D+)(\d{4})')## 1July-1August
        pattern2 = re.compile(r'(\d{1,2})[-\u2013](\d{1,2})(\D+)(\d{4})')##1-3July
        pattern3 = re.compile(r'(\d{1,2})(\D+)(\d{4})')##2 july
        pattern7 =  re.compile(r'([\d{1,2}]+)(\D+)[&and](\d{1,2})(\D+)(\d{4})') ##1,2,3 &/and July 
        pattern8 =  re.compile(r'([\d{1,2}]+)[-\u2013](\d{1,2})(\D+)[&and](\d{1,2})[-\u2013](\d{1,2})(\D+)(\d{4})') ##1,2,3 &/and July 
        pattern9 = re.compile(r'([\d{1,2}]+)and(\d{1,2})(\D+)(\d{4})') 
        pattern10 = re.compile(r'(\d{1,2})[-\u2013](\d{1,2})(\D+)&(\d{1,2})(\D+)[-\u2013](\d{1,2})(\D+)(\d{4})')

        pattern4 = re.compile(r'([\d,]+)[&and]*(\d{1,2})(\D+)(\d{4})') ##1,2,3 &/and July 
        pattern5 = re.compile(r'(\w+)(\d{4})') # july 2023 
        pattern6 = re.compile(r'(\d{1,2})[-\u2013](\d{1,2})[&and]*(\d{1,2})[-\u2013](\d{1,2})(\w+)(\d{4})')
        patterns = [pattern0,pattern1,pattern2,pattern3,pattern5]
        if 'and' in date or '&' in date :
            patterns = [pattern9,pattern7,pattern4]
            if "–" in date:
                patterns = [pattern6,pattern8,pattern10]
        for pattern in patterns:
            
            
            match = re.search(pattern,date)
            if not match is None:
                if pattern==pattern0:
                    day1 ,month1 ,year1,day2,month2,year2 = match.groups()
                    return day1 ,month1 ,year1,day2,month2,year2,0
                elif pattern == pattern1:
                    day1, month1, day2, month2, year = match.groups()     
                    return day1,month1,day2,month2,year,1
                elif pattern == pattern2:
                    day1, day2, month, year = match.groups()
                    return day1,day2,month,year,2
                elif pattern == pattern3:
                    day, month, year = match.groups()
                    return day,month,year,3
                elif pattern  == pattern4:
                    days,days2, month, year = match.groups()
                    return days+','+days2,month,year,4 
                elif pattern == pattern5:
                    month, year = match.groups()
                    return month,year,5
                elif pattern  == pattern6:
                    days11,days12,days21,days22, month, year = match.groups()
                    return days11+','+days12+','+days21+','+days22,month,year,6 
                elif pattern  == pattern7:
                    days11,month1,day2, month2, year = match.groups()
                    return days11,month1,day2,month2,year,7
                elif pattern  == pattern8:
                    days11,days12,month1,days21,days22, month2, year = match.groups()
                    return days11+','+days12,month1,days21+','+days22,month2,year,8
                elif pattern  == pattern9:
                    days11,days12,month, year = match.groups()
                    return days11+','+days12,month,year,9
                elif pattern  == pattern10:
                    days11, days12,month1,days13,month1,days21,month2,year = match.groups()
                    return days11+','+days12+','+days13,month1,days21,month2,year,10
    def fix_form(self,sports_news):    
        new_df = pd.DataFrame()
        sports_news_ = [news for news in sports_news if not news==" "]
        for event in sports_news_:
            event_list = event.split("\n")
            event = event_list[0]
            if ("[CANCELLED]" in event) or ("[POSTPONED]" in event):
                continue
            date=event_list[1].split("|")[0]
            date = date.split(" ")
            date = [i for i in date if not i ==' ']
            date = "".join(date)
            date_tuple = self.extract_date(date)
            if date_tuple[-1]==0: 
                days1 = [i for i in range(int(date_tuple[0]),32)]
                days2 = [i for i in range(1,int(date_tuple[3])+1)]
                dff = pd.DataFrame({"year":[date_tuple[2],date_tuple[-2]],
                                    "month":[self.mapping[date_tuple[1]],self.mapping[date_tuple[4]]],
                                    "days":[days1,days2],
                                    "event": event }
                                    )
                new_df = pd.concat([new_df,dff])
            elif date_tuple[-1]==1:
                days1 = [i for i in range(int(date_tuple[0]),29)]
                days2 = [i for i in range(1,int(date_tuple[2])+1)]
                dff = pd.DataFrame({"year":[date_tuple[-2],date_tuple[-2]],
                                    "month":[self.mapping[date_tuple[1]],self.mapping[date_tuple[3]]],
                                    "days":[days1,days2],
                                    "event": event })
                new_df = pd.concat([new_df,dff])
            
            
            if date_tuple[-1]==2:
                days = [i for i in range(int(date_tuple[0]),int(date_tuple[1])+1)]
                dff = pd.DataFrame({"year":[date_tuple[-2]],
                                    "month":[self.mapping[date_tuple[2]]],
                                    "days":[days],
                                    "event": event })
                new_df = pd.concat([new_df,dff])
                
            
            if date_tuple[-1]==3:        
                dff = pd.DataFrame({"year":[date_tuple[-2]],
                                    "month":[self.mapping[date_tuple[1]]],
                                    "days":[date_tuple[0]],
                                    "event": event })
                new_df = pd.concat([new_df,dff])
            
            if date_tuple[-1]==4:        
                days = date_tuple[0].split(',')
                days =[ int(i) for i in days]
                dff = pd.DataFrame({"year":[date_tuple[-2]],
                                    "month":[self.mapping[date_tuple[-3]]],
                                    "days":[days],
                                    "event": event })
                new_df = pd.concat([new_df,dff])
            
            if date_tuple[-1]==5:        
                days = [i for i in range(1,29)]
                dff = pd.DataFrame({"year":[date_tuple[-2]],
                                    "month":[self.mapping[date_tuple[-3]]],
                                    "days":[days],
                                    "event": event })
                new_df = pd.concat([new_df,dff])
            
            if date_tuple[-1]==6:        
                days = date_tuple[0].split(',')
                days =[ int(i) for i in days]
                dff = pd.DataFrame({"year":[date_tuple[-2]],
                                    "month":[self.mapping[date_tuple[-3]]],
                                    "days":[days],
                                    "event": event })
                new_df = pd.concat([new_df,dff])
            
            if date_tuple[-1]==7:  
                days = date_tuple[0].split(',')
                days1 =[ int(i) for i in days]
                dff = pd.DataFrame({"year":[date_tuple[-2],date_tuple[-2]],
                                    "month":[self.mapping[date_tuple[1]],self.mapping[date_tuple[-3]]],
                                    "days":[days1,date_tuple[2]],
                                    "event": event })
                new_df = pd.concat([new_df,dff])
                
            if date_tuple[-1]==8:  
                days = date_tuple[0].split(',')
                days1 =[ int(i) for i in days]
                days = date_tuple[2].split(',')
                days2 =[ int(i) for i in days]
                dff = pd.DataFrame({"year":[date_tuple[-2],date_tuple[-2]],
                                    "month":[self.mapping[date_tuple[1]],self.mapping[date_tuple[-3]]],
                                    "days":[days1,date_tuple[2]],
                                    "event": event })
                new_df = pd.concat([new_df,dff])
            if date_tuple[-1]==9:  
                days = date_tuple[0].split(',')
                days =[ int(i) for i in days]
                dff = pd.DataFrame({"year":[date_tuple[-2]],
                                    "month":[self.mapping[date_tuple[1]]],
                                    "days":[days],
                                    "event": event })
                new_df = pd.concat([new_df,dff])
            if date_tuple[-1]==10:  
                days = date_tuple[0].split(',')
                days.append(date_tuple[2])
                days1 =[ int(i) for i in days]
                dff = pd.DataFrame({"year":[date_tuple[-2],date_tuple[-2]],
                                    "month":[self.mapping[date_tuple[1]],self.mapping[date_tuple[-3]]],
                                    "days":[days1,int(date_tuple[2])],
                                    "event": event })
                new_df = pd.concat([new_df,dff])
        return new_df 
    def expand_df(self):
        df = pd.read_csv("Scraping\\Sports_\\compressed_sports_df.csv")
        new_df=pd.DataFrame() 
        for _, row in df.iterrows():
            if isinstance(row['days'], str) and row['days'].startswith('['):
                day_list = ast.literal_eval(row['days'])
                for day in day_list:
                    df1 = pd.DataFrame({"year":[row['year']],"month":[row['month']],'day':[day],'event':[row['event']]})
                    new_df = pd.concat([new_df,df1])
        new_df['date'] = pd.to_datetime(new_df[['year', 'month', 'day']])
       

        df_grouped = new_df.groupby('date').agg({'event': list}).reset_index()
        df_grouped['event'] = df_grouped['event'].apply(lambda x: list(set(x)))
        return df_grouped
        
    def run(self):
        with open(self.file_path) as fr:
            sports_news = json.load(fr)
        new_df = self.fix_form(sports_news)
        compressed_df = new_df.sort_values(by=['year', 'month']).reset_index(drop=True)
        compressed_df.to_csv('Scraping\\Sports_\\compressed_sports_df.csv',index=False)
        new_df = self.expand_df()
        new_df.to_csv(self.df_path,index=False)
