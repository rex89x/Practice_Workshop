from openai import OpenAI
import os

# ✅ 確保 API Key 正確讀取\
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("❌ OpenAI API Key 未設置，請確認環境變數！")


# ✅ 初始化 OpenAI Client（這樣 API Key 會自動讀取）
client = OpenAI(api_key=OPENAI_API_KEY)

# 讀取 OpenAI API Key
# client = OpenAI()

def summarize_text(text):
    """使用 OpenAI GPT-4 進行文字摘要"""
    if not text.strip():
        return "⚠️ 無有效的文字可摘要"
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "你是一個網路摘要機器人。"},
                {"role": "user", "content": f"請摘要以下內容:\n{text}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ OpenAI API 發生錯誤: {e}"

# 測試
#if __name__ == "__main__":
    #test_text = "這是一段測試文字，使用 OpenAI 進行摘要測試。"
    #summary = summarize_text(test_text)
    #print("🔍 摘要結果:\n", summary)