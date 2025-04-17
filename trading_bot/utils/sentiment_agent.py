# ✅ sentiment_agent.py - 情緒判斷模組（OpenAI 分析）
import os
import openai

class SentimentAgent:
    @classmethod
    def load_api_key(cls):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    @classmethod
    def analyze(cls, headline: str) -> str:
        cls.load_api_key()

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "你是一位財經分析師，只回答 BUY 或 SELL"},
                    {"role": "user", "content": f"以下為最新市場消息：{headline}\n請給我你的投資判斷："}
                ],
                temperature=0.5,
                max_tokens=10
            )
            content = response["choices"][0]["message"]["content"].strip().upper()
            if "BUY" in content:
                return "BUY"
            elif "SELL" in content:
                return "SELL"
            else:
                return "HOLD"
        except Exception as e:
            print(f"❌ OpenAI 分析錯誤：{e}")
            return "HOLD"
