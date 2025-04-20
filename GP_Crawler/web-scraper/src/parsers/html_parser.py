from bs4 import BeautifulSoup

class HtmlParser:
    def parse(self, html_content):
        """
        解析HTML內容並返回BeautifulSoup物件
        """
        return BeautifulSoup(html_content, 'html.parser')
    
    def extract_toxic_substances_list(self, soup):
        """
        從主頁面提取有毒物質列表
        """
        substances = []
        # 假設列表在table或特定容器內
        items = soup.select('.cha_ul li')
        
        for item in items:
            a_tag = item.select_one('a')
            if a_tag:
                name = a_tag.get_text(strip=True)
                url = a_tag.get('href')
                # 處理相對URL
                if url and not url.startswith('http'):
                    url = f"https://www.cha.gov.tw/{url}"
                
                substances.append({
                    'name': name,
                    'url': url
                })
        
        return substances
    
    def extract_substance_details(self, soup):
        """
        從詳細頁面提取物質的詳細資訊
        """
        details = {}
        
        # 提取表格內容
        tables = soup.select('.rwd-table')
        for table in tables:
            rows = table.select('tr')
            for row in rows:
                # 嘗試獲取標題和內容
                headers = row.select('th')
                cells = row.select('td')
                
                if headers and cells:
                    for i, header in enumerate(headers):
                        if i < len(cells):
                            key = header.get_text(strip=True)
                            value = cells[i].get_text(strip=True)
                            details[key] = value
        
        return details