import telebot
from telebot import types
import logging
from config import BOT_TOKEN, LOGS_CHANNEL
from db import update_user_data
from handlers import register_all_handlers

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# Logs function
def log_message(log_type: str, message: str, user_id: int = None, chat_id: int = None, 
                username: str = None, first_name: str = None, chat_title: str = None, 
                extra_data: str = ""):
    try:
        import time
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        log_text = f"""🪵 <b>LOG TYPE:</b> {log_type}
⏰ <b>TIME:</b> <code>{timestamp}</code>"""

        if user_id:
            log_text += f"\n👤 <b>USER ID:</b> <code>{user_id}</code>"
        
        if first_name:
            log_text += f"\n👨‍💼 <b>NAME:</b> {first_name}"
        
        if username:
            log_text += f"\n📎 <b>USERNAME:</b> @{username}" if username else "\n📎 <b>USERNAME:</b> No username"
        
        if chat_id:
            if chat_id == user_id:
                log_text += f"\n💬 <b>CHAT:</b> Private Chat"
            else:
                log_text += f"\n💬 <b>CHAT ID:</b> <code>{chat_id}</code>"
        
        if chat_title:
            log_text += f"\n🏷️ <b>GROUP:</b> {chat_title}"
        
        if message:
            log_text += f"\n📝 <b>MESSAGE:</b> {message}"
        
        if extra_data:
            log_text += f"\n📊 <b>EXTRA:</b> {extra_data}"

        bot.send_message(LOGS_CHANNEL, log_text, parse_mode="HTML")
        
    except Exception as e:
        logger.exception("log_message failed: %s", e)

# Register all handlers
register_all_handlers(bot)

# Start message
print("🤖 Bot is starting with modular structure...")

if __name__ == "__main__":
    bot.infinity_polling(timeout=60, long_polling_timeout=5)
