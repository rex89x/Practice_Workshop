from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
import os
import time

# 讀取 Azure OCR API Key 和 Endpoint
AZURE_OCR_ENDPOINT = os.getenv("AZURE_OCR_ENDPOINT")  # 例如 "https://your-region.api.cognitive.microsoft.com/"
AZURE_OCR_API_KEY = os.getenv("AZURE_OCR_API_KEY")  # 你的 API Key

# 初始化 Azure OCR 客戶端
computervision_client = ComputerVisionClient(AZURE_OCR_ENDPOINT, CognitiveServicesCredentials(AZURE_OCR_API_KEY))

def recognize_text(image_path):
    """ 使用 Azure OCR API 進行影像文字辨識 """
    with open(image_path, "rb") as image_stream:
        read_response = computervision_client.read_in_stream(image_stream, raw=True)

    # 取得請求 ID
    read_operation_location = read_response.headers["Operation-Location"]
    operation_id = read_operation_location.split("/")[-1]

    # 輪詢 OCR 進度
    print("🔄 正在處理 OCR，請稍候...")
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in [OperationStatusCodes.running, OperationStatusCodes.not_started]:
            break
        time.sleep(1)  # 等待 OCR 完成

    # 解析 OCR 結果
    if read_result.status == OperationStatusCodes.succeeded:
        extracted_text = []
        for page in read_result.analyze_result.read_results:
            for line in page.lines:
                extracted_text.append(line.text)
        return "\n".join(extracted_text)
    else:
        return "⚠️ OCR 辨識失敗，請檢查圖片是否清晰"

# 測試 OCR
if __name__ == "__main__":
    image_path = "test.png"  # 你可以更換成其他影像
    if not os.path.exists(image_path):
        print(f"❌ 找不到圖片檔案: {image_path}")
    else:
        result = recognize_text(image_path)
        print("\n🔍 OCR 辨識結果:\n", result)