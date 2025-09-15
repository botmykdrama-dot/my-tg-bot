import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token from environment variable
BOT_TOKEN = os.environ.get('BOT_TOKEN')
PORT = int(os.environ.get('PORT', 8080))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}! I'm a simple bot running on Koyeb. 🚀\n\n"
        f"Available commands:\n"
        f"/start - Show this message\n"
        f"/help - Get help\n"
        f"/ping - Check if bot is alive\n"
        f"Send me any message and I'll echo it back!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = """
🤖 *Simple Telegram Bot*

*Commands:*
/start - Start the bot
/help - Show this help message
/ping - Check bot status

*Features:*
• Echo messages back to you
• Responds to all text messages
• Deployed on Koyeb platform

Just send me any text and I'll echo it back! 📝
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Respond with pong to check if bot is alive."""
    await update.message.reply_text("🏓 Pong! Bot is alive and running on Koyeb!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    user_message = update.message.text
    response = f"You said: {user_message}\n\n🔄 Echoed back from Koyeb!"
    await update.message.reply_text(response)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer."""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

def main() -> None:
    """Start the bot."""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN environment variable is not set!")
        return

    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("ping", ping))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Add error handler
    application.add_error_handler(error_handler)

    # Start the bot with webhook for Koyeb deployment
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"https://your-app-name.koyeb.app/{BOT_TOKEN}",
        url_path=f"/{BOT_TOKEN}",
        drop_pending_updates=True
    )

if __name__ == '__main__':
    main()
