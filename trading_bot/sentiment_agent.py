# 版本標籤：Unified-Team-v2.4.6-AutoOrderEnabled（來源：UnifiedTeam_Backup_20250415_2354.zip）
import logging
import requests
from textblob import TextBlob

# 初始化日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_sentiment(text: str) -> str:
    """
    使用 TextBlob 对文本进行情绪分析
    :param text: str，待分析文本
    :return: str，分析结果 ('BUY', 'SELL', 'HOLD')
    """
    try:
        # 使用 TextBlob 分析情绪
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity  # 情感极性值（-1 到 1，负值表示负面情绪，正值表示正面情绪）

        # 根据情感极性返回决策
        if polarity > 0.1:
            decision = "BUY"
        elif polarity < -0.1:
            decision = "SELL"
        else:
            decision = "HOLD"

        logger.info(f"📊 情绪分析：{text} | 极性：{polarity:.2f} | 决策：{decision}")
        return decision

    except Exception as e:
        logger.error(f"❌ 情绪分析失败：{e}")
        logger.debug(e, exc_info=True)
        return "HOLD"  # 在异常情况下返回 "HOLD" 作为默认决策

def analyze_sentiment_from_source(source: str) -> str:
    """
    从外部源获取文本并分析情绪
    :param source: str，外部数据源 URL
    :return: str，分析结果 ('BUY', 'SELL', 'HOLD')
    """
    try:
        # 从外部源获取文本数据
        response = requests.get(source)
        if response.status_code == 200:
            text = response.text
            return analyze_sentiment(text)
        else:
            logger.warning(f"⚠️ 从 {source} 获取数据失败，状态码：{response.status_code}")
            return "HOLD"
    except Exception as e:
        logger.error(f"❌ 从 {source} 获取数据失败：{e}")
        logger.debug(e, exc_info=True)
        return "HOLD"
