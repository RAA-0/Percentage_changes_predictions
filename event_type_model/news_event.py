from Scraping.ScraperFactory import ScraperFactory

class NewsEvent():
    def __init__(self):
        pass
    
    def detect_event(self,date):
        events=[]
        f = ScraperFactory()
        for event in ['health','sports','disruption','conference']:
            conf=f.create_config(event)
            events.extend(conf.detect_event(date))
        return events 
    