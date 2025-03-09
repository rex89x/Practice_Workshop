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

    return {"text": recognized_text, "summary": summary}

@app.get("/", response_class=HTMLResponse)
async def homepage():
    """顯示上傳介面"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>OCR Upload</title>
    </head>
    <body>
        <h2>上傳圖片進行 OCR + AI 總結</h2>
        <form action="/upload/" method="post" enctype="multipart/form-data">
            <input type="file" name="file">
            <button type="submit">上傳</button>
        </form>
    </body>
    </html>
    """

# 執行指令 (本地測試)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)