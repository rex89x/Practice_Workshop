import json
import os
from ..utils.http_client import HttpClient
from ..parsers.html_parser import HtmlParser

class ToxicSubstancesScraper:
    def __init__(self, base_url="https://www.cha.gov.tw/sp-toch-list-1.html"):
        self.base_url = base_url
        self.http_client = HttpClient()
        self.parser = HtmlParser()
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                      "data", "output")
        
        # 創建輸出目錄（如果不存在）
        os.makedirs(self.output_dir, exist_ok=True)
    
    def scrape(self):
        """
        爬取有毒物質列表和詳細信息
        """
        # 獲取主頁面HTML
        html_content = self.http_client.get(self.base_url)
        if not html_content:
            print("無法獲取主頁面內容")
            return
        
        # 解析並提取物質列表
        soup = self.parser.parse(html_content)
        substances = self.parser.extract_toxic_substances_list(soup)
        
        if not substances:
            print("未找到任何有毒物質")
            return
        
        print(f"找到 {len(substances)} 種有毒物質")
        
        # 為每個物質爬取詳細資訊
        for i, substance in enumerate(substances):
            print(f"正在處理 ({i+1}/{len(substances)}): {substance['name']}")
            
            if substance.get('url'):
                detail_html = self.http_client.get(substance['url'])
                if detail_html:
                    detail_soup = self.parser.parse(detail_html)
                    details = self.parser.extract_substance_details(detail_soup)
                    substance['details'] = details
            
        # 保存為JSON文件
        self._save_to_json(substances)
        
        return substances
    
    def _save_to_json(self, data):
        """
        將數據保存為JSON文件
        """
        output_path = os.path.join(self.output_dir, "toxic_substances.json")
        
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        
        print(f"數據已保存至: {output_path}")