document.addEventListener('DOMContentLoaded', function() {
    // 元素參照
    const startButton = document.getElementById('start-button');
    const refreshButton = document.getElementById('refresh-button');
    const downloadButton = document.getElementById('download-button');
    const sourceSelect = document.getElementById('source');
    const loadingSection = document.getElementById('loading');
    const resultSection = document.getElementById('result');
    
    // 目前的檔案名稱
    let currentFilename = null;
    
    // 開始爬取按鈕事件
    startButton.addEventListener('click', function() {
        const selectedSource = sourceSelect.value;
        
        if (!selectedSource) {
            alert('請選擇要爬取的來源網站');
            return;
        }
        
        // 顯示載入畫面
        loadingSection.classList.remove('hidden');
        resultSection.classList.add('hidden');
        startButton.disabled = true;
        
        // 發送爬蟲請求
        fetch('/api/scrape', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                source: selectedSource
            })
        })
        .then(response => response.json())
        .then(data => {
            loadingSection.classList.add('hidden');
            
            if (data.success) {
                resultSection.classList.remove('hidden');
                currentFilename = data.filename;
            } else {
                alert('爬取失敗: ' + data.message);
            }
            
            startButton.disabled = false;
        })
        .catch(error => {
            loadingSection.classList.add('hidden');
            alert('發生錯誤: ' + error.message);
            startButton.disabled = false;
        });
    });
    
    // 下載按鈕事件
    downloadButton.addEventListener('click', function() {
        if (currentFilename) {
            window.location.href = `/api/download/${currentFilename}`;
        } else {
            alert('沒有可供下載的檔案');
        }
    });
    
    // 重新整理按鈕事件
    refreshButton.addEventListener('click', function() {
        loadingSection.classList.add('hidden');
        resultSection.classList.add('hidden');
        currentFilename = null;
    });
});