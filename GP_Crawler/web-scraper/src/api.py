import os
import json
import time
import datetime
from flask import Flask, request, jsonify, send_file
from scrapers.toxic_substances_scraper import ToxicSubstancesScraper

app = Flask(__name__, static_folder='static')

@app.route('/api/scrape', methods=['POST'])
def scrape():
    try:
        source = request.json.get('source')
        
        # 根據來源選擇不同爬蟲
        if source == 'chemical_management':
            scraper = ToxicSubstancesScraper()
            data = scraper.scrape()
            
            # 生成有時間戳的文件名
            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            filename = f"scraper_{timestamp}.json"
            filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                   "data", "output", filename)
            
            # 保存JSON數據
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return jsonify({
                'success': True,
                'message': '爬蟲完成',
                'filename': filename
            })
        else:
            return jsonify({
                'success': False,
                'message': '不支援的爬蟲來源'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'爬蟲過程中發生錯誤: {str(e)}'
        }), 500

@app.route('/api/download/<filename>', methods=['GET'])
def download(filename):
    try:
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                               "data", "output", filename)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'下載文件時發生錯誤: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)