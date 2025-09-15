import os
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from plugins.start import register_start_handler
from helpers.help import register_help_handler

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token from environment variable
BOT_TOKEN = os.environ.get('BOT_TOKEN')
PORT = int(os.environ.get('PORT', 8080))

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo any text message back to user."""
    user_message = update.message.text
    response = f"You said: {user_message}\n\n🔄 Echoed back from Koyeb!"
    await update.message.reply_text(response)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors."""
    logger.error(f"Update {update} caused error {context.error}")

def main():
    """Main function to start the bot."""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN environment variable is not set!")
        return

    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Register handlers from plugins and helpers
    register_start_handler(application)
    register_help_handler(application)
    
    # Add echo handler for regular messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Add error handler
    application.add_error_handler(error_handler)

    # Start the bot with polling
    logger.info("Starting bot with polling...")
    application.run_polling(
        poll_interval=1.0,
        timeout=10,
        bootstrap_retries=-1,
        read_timeout=30,
        write_timeout=30,
        connect_timeout=30,
        pool_timeout=30,
        drop_pending_updates=True
    )

if __name__ == '__main__':
    main()
