import logging
import smtplib
from email.mime.text import MIMEText
from telegram import Bot
from telegram.error import TelegramError
import os

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AlertNotifier:
    def __init__(self, email_server="localhost", email_from="alert-bot@example.com", email_to="your_email@example.com"):
        self.email_server = email_server
        self.email_from = email_from
        self.email_to = email_to

        # 加载环境变量
        self.telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

    def send_email(self, subject, message):
        """
        发送电子邮件通知
        :param subject: 邮件主题
        :param message: 邮件内容
        """
        try:
            msg = MIMEText(message)
            msg["Subject"] = subject
            msg["From"] = self.email_from
            msg["To"] = self.email_to

            # 配置邮件服务器
            with smtplib.SMTP(self.email_server) as smtp:
                smtp.send_message(msg)
            logger.info(f"📤 已发送邮件通知：{subject}")
        except Exception as e:
            logger.error(f"❌ 发送邮件通知失败：{e}")

    def send_telegram_message(self, message):
        """
        发送 Telegram 消息通知
        :param message: 消息内容
        """
        if not self.telegram_token or not self.telegram_chat_id:
            logger.error("❌ Telegram 配置不完整，无法发送消息。")
            return
        
        try:
            bot = Bot(token=self.telegram_token)
            bot.send_message(chat_id=self.telegram_chat_id, text=message)
            logger.info(f"📱 已发送 Telegram 消息：{message}")
        except TelegramError as e:
            logger.error(f"❌ 发送 Telegram 消息失败：{e}")

    def send_alert(self, subject, message):
        """
        发送警告通知（支持邮件和 Telegram）
        :param subject: 通知的主题
        :param message: 通知的内容
        """
        # 发送邮件通知
        self.send_email(subject, message)

        # 发送 Telegram 消息通知
        self.send_telegram_message(message)

if __name__ == "__main__":
    # 创建通知实例
    notifier = AlertNotifier()

    # 示例通知
    notifier.send_alert(
        subject="警告通知 - 系统故障",
        message="系统出现故障，请尽快检查并修复。"
    )
