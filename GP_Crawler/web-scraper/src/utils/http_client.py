import requests
import time
import random

class HttpClient:
    def __init__(self, timeout=30, headers=None):
        self.timeout = timeout
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
    
    def get(self, url):
        """
        發送GET請求並返回響應內容
        """
        try:
            # 隨機延遲，避免過快請求
            time.sleep(random.uniform(1, 3))
            
            response = self.session.get(
                url, 
                headers=self.headers,
                timeout=self.timeout
            )
            response.raise_for_status()  # 檢查請求是否成功
            return response.text
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            return None

    def post(self, url, data):
        response = self.session.post(
            url, 
            json=data, 
            headers=self.headers,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()