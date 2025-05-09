import aiohttp
import asyncio
import os

#AZURE_OCR_ENDPOINT = os.getenv("AZURE_OCR_ENDPOINT")
#AZURE_OCR_KEY = os.getenv("AZURE_OCR_KEY")

async def extract_text_from_image_read_api(image_bytes: bytes) -> str:
    analyze_url = f"{AZURE_OCR_ENDPOINT}/vision/v3.2/read/analyze"

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_OCR_KEY,
        "Content-Type": "application/octet-stream",
    }

    async with aiohttp.ClientSession() as session:
        # 發送圖片
        async with session.post(analyze_url, headers=headers, data=image_bytes) as response:
            if response.status != 202:
                text = await response.text()
                raise Exception(f"Azure Read API failed: {response.status}, {text}")

            operation_url = response.headers.get("Operation-Location")
            if not operation_url:
                raise Exception("Missing Operation-Location in response headers")

        # 輪詢結果
        status = "running"
        while status in ["running", "notStarted"]:
            await asyncio.sleep(1)
            async with session.get(operation_url, headers={"Ocp-Apim-Subscription-Key": AZURE_OCR_KEY}) as result_response:
                if result_response.status != 200:
                    text = await result_response.text()
                    raise Exception(f"Failed to get result: {result_response.status}, {text}")
                result = await result_response.json()
                status = result.get("status")

        if status != "succeeded":
            raise Exception(f"OCR did not succeed: {status}")

    # 解析結果
    lines = []
    analyze_result = result.get("analyzeResult", {})
    for read_result in analyze_result.get("readResults", []):
        for line in read_result.get("lines", []):
            lines.append(line.get("text", ""))

    return "\n".join(lines)

# 測試 OCR
if __name__ == "__main__":
    async def main():
        image_path = "test.png"  # 改成你的檔名
        if not os.path.exists(image_path):
            print(f"找不到檔案：{image_path}")
            return

        with open(image_path, "rb") as f:
            image_bytes = f.read()

        try:
            text = await extract_text_from_image_read_api(image_bytes)
            print("OCR 結果：\n")
            print(text)
        except Exception as e:
            print(f"OCR 發生錯誤: {e}")

    asyncio.run(main())