import openai
import os

# 讀取 OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def summarize_text(text):
    """使用 OpenAI GPT-4 進行文字摘要"""
    if not text.strip():
        return "⚠️ 無有效的文字可摘要"
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": f"請摘要以下內容:\n{text}"}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ OpenAI API 發生錯誤: {e}"

# 測試
if __name__ == "__main__":
    test_text = "這是一段測試文字，使用 OpenAI 進行摘要測試。"
    summary = summarize_text(test_text)
    print("🔍 摘要結果:\n", summary)