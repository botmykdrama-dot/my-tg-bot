from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
import logging

logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    user = update.effective_user
    welcome_message = f"""
Hi {user.mention_html()}! I'm a simple bot running on Koyeb. 🚀

Available commands:
/start - Show this welcome message
/help - Get detailed help information
/ping - Check if bot is alive

✨ Features:
- Echo messages back to you
- Responds to all text messages
- Deployed on Koyeb platform

Just send me any text and I'll echo it back! 📝
    """
    
    await update.message.reply_html(welcome_message.strip())
    logger.info(f"Start command used by user: {user.first_name} (@{user.username})")

async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /ping command."""
    await update.message.reply_text("🏓 Pong! Bot is alive and running on Koyeb!")
    logger.info("Ping command executed")

def register_start_handler(application):
    """Register start-related command handlers."""
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("ping", ping_command))
    logger.info("Start plugin handlers registered")
