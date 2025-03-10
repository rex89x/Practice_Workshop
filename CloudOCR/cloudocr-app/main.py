from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
import shutil
import os

from ocr import recognize_text
from summary import summarize_text

app = FastAPI()

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    """上傳圖片並進行 OCR + 總結"""
    file_path = f"temp_{file.filename}"
    
    # 存檔圖片
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # OCR 文字辨識
    recognized_text = recognize_text(file_path)
    
    # OpenAI 總結
    summary = summarize_text(recognized_text)

    # 刪除暫存圖片
    os.remove(file_path)

    html_content = f"""
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>OCR AI 結果</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script>
            tailwind.config = {{
                theme: {{
                    extend: {{}}
                }}
            }};
        </script>
    </head>
    <body class="bg-gray-50 flex flex-col items-center justify-center min-h-screen p-6">
        <div class="bg-white p-8 rounded-lg shadow-lg max-w-2xl w-full text-center">
            <h2 class="text-2xl font-bold text-gray-800">OCR + AI 總結結果</h2>
            <div class="mt-4 text-left">
                <h3 class="text-lg font-semibold text-gray-900">🔍 辨識結果：</h3>
                <p class="bg-gray-100 p-4 rounded-md text-gray-800">{recognized_text}</p>
            </div>
            <div class="mt-4 text-left">
                <h3 class="text-lg font-semibold text-gray-900">✍️ AI 總結：</h3>
                <p class="bg-gray-100 p-4 rounded-md text-gray-800">{summary}</p>
            </div>
            <a href="/" class="mt-6 inline-block bg-blue-500 text-white px-6 py-2 rounded-md hover:bg-blue-700 transition">🔄 回到首頁</a>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/", response_class=HTMLResponse)
async def homepage():
    """顯示美化的上傳介面"""
    return """
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>OCR AI 上傳系統</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-100 flex flex-col items-center justify-center min-h-screen p-6">
        <div class="bg-white p-8 rounded-lg shadow-lg max-w-lg text-center">
            <h2 class="text-2xl font-bold text-gray-700">上傳圖片進行 OCR + AI 總結</h2>
            <form action="/upload/" method="post" enctype="multipart/form-data" class="mt-6">
                <input type="file" name="file" required
                    class="block w-full text-sm text-gray-600 file:mr-4 file:py-2 file:px-4 
                           file:rounded-md file:border-0 file:text-sm file:font-semibold 
                           file:bg-blue-600 file:text-white hover:file:bg-blue-700">
                <button type="submit" class="mt-4 w-full bg-blue-500 text-white py-2 rounded-md hover:bg-blue-700 transition">📤 上傳</button>
            </form>
        </div>
    </body>
    </html>
    """

# 執行指令 (本地測試)
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="127.0.0.1", port=port, reload=True)