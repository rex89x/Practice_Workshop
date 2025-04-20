# web-scraper/src/main.py

from api import app
from scrapers.base_scraper import BaseScraper
from parsers.html_parser import HtmlParser
from utils.http_client import HttpClient
from utils.data_cleaner import clean_data
from models.item import Item
from scrapers.toxic_substances_scraper import ToxicSubstancesScraper

def main():
    print("開始爬取有毒物質數據...")
    
    # 初始化爬蟲
    scraper = ToxicSubstancesScraper()
    
    # 執行爬蟲
    scraper.scrape()
    app.run()
    
    print("爬蟲任務完成！")

if __name__ == "__main__":
    main()