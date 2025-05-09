import asyncio
from openai import AsyncOpenAI
import os

#openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_summary(text: str, length: str = None) -> str:
    if not text:
        return "No text found in image."

    prompt = f"Summarize the following text."
    if length in ["short", "medium", "long"]:
        prompt += f" Make it {length}."
    prompt += f"\n\n{text}"

    response = await openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful summarizer."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )

    summary_text = response.choices[0].message.content.strip()
    return summary_text

# 測試程式
if __name__ == "__main__":
    async def main():
        # 測試文字（你可以換成 OCR 的輸出結果）
        test_text = """
        若能避開猛烈的狂喜，自然也不會有悲痛的來襲。
        —— 太宰治《人間失格》
        這段話出自日本作家太宰治的名著，表達了人對情感波動的深刻體會。
        """

        try:
            summary = await generate_summary(test_text, length="short")
            print("摘要結果：\n")
            print(summary)
        except Exception as e:
            print(f"摘要發生錯誤: {e}")

    asyncio.run(main())