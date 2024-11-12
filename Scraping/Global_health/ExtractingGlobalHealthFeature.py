import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

class GlobalHealthExtractor:
    def __init__(self,news_data,file_path,health_terms,df_path):
        self.news_data = news_data
        self.file_path = file_path
        self.health_terms = health_terms
        self.df_path = df_path 
    
    def run(self):
        news_df=self.dataframe_creator()
        self.health_score(news_df,threshold=0.1)
        self.global_health_crisis(threshold=6)
    
    def dataframe_creator(self):
        news_list = []
        for year, months in self.news_data.items():
            for month, days in months.items():
                for day, headlines in days.items():
                    for headline in headlines:
                        news_list.append({'year': year, 'month': month, 'day': day, 'headline': headline})
        news_df = pd.DataFrame(news_list)
        return news_df
    
    def health_score(self,news_df,threshold):
        tfidf_vectorizer = TfidfVectorizer(stop_words='english', lowercase=True)
        tfidf_matrix = tfidf_vectorizer.fit_transform(news_df['headline'])
        terms_idx = [tfidf_vectorizer.vocabulary_.get(term) for term in self.health_terms if term in tfidf_vectorizer.vocabulary_]
        news_df['health_score'] = tfidf_matrix[:, terms_idx].sum(axis=1)
        news_df['global_health_issue'] = (news_df['health_score'] > threshold).astype(int)
        news_df.to_csv(self.file_path, index = False )

    def global_health_crisis(self,threshold):
        df = pd.read_csv(self.file_path, header=None)
        df.columns = ['year', 'month', 'day', 'headline', 'health_score', 'global_health_issue']

        df['year'] = pd.to_numeric(df['year'], errors='coerce').astype('Int64') 
        df['month'] = pd.to_numeric(df['month'], errors='coerce').astype('Int64')
        df['day'] = pd.to_numeric(df['day'], errors='coerce').astype('Int64')

        df['date'] = pd.to_datetime(df[['year', 'month', 'day']].astype(str).agg('-'.join, axis=1), errors='coerce')
        df.set_index('date', inplace=True)
        df.columns = ['year', 'month', 'day', 'headline', 'health_score', 'global_health_issue']

        df['global_health_issue'] = pd.to_numeric(df['global_health_issue'], errors='coerce')

        monthly_health_crisis = df['global_health_issue'].resample('M').sum()

        threshold = 6

        monthly_health_crisis = pd.to_numeric(monthly_health_crisis, errors='coerce')

        monthly_health_crisis_feature = (monthly_health_crisis >= threshold).astype(int)

        monthly_df = pd.DataFrame({
            'month_end': monthly_health_crisis.index,
            'health_crisis_month': monthly_health_crisis_feature
        })

        monthly_df.reset_index(drop=True, inplace=True)
        monthly_df.to_csv(self.df_path,index=False)

