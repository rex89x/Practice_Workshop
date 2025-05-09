from fastapi import FastAPI, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional
import shutil
import os

from ocr import extract_text_from_image_read_api
from summary import generate_summary
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 可以根據需求限制來源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process-image")
async def process_image(
    image: UploadFile,
    summary_length: Optional[str] = Form(None)
):
    if not image:
        raise HTTPException(status_code=400, detail="Image file is required.")

    try:
        # OCR: 擷取文字
        image_bytes = await image.read()
        extracted_text = await extract_text_from_image_read_api(image_bytes)

        # 摘要: 根據 summary_length 控制長度
        summary = await generate_summary(extracted_text, summary_length)

        return JSONResponse(
            content={
                "extracted_text": extracted_text,
                "summary": summary
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

# 執行指令 (本地測試)
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="127.0.0.1", port=port, reload=True)