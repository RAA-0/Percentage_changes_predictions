from Scraping.confernces_scraping import ConferenceScraper
from Scraping.disruptions_scraper import DisruptionsScraper
from Scraping.global_health_scraper import GlobalHealthScraper
from Scraping.sports_scraper import SportsScraper

class ScraperFactory:
    @staticmethod
    def create_config(config_type):
        if config_type == "health":
            return GlobalHealthScraper()
        elif config_type == "disruption":
            return DisruptionsScraper()
        elif config_type == "sports":
            return SportsScraper()
        elif config_type == "conference":
            return ConferenceScraper()
        
        else:
            return None 