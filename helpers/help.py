from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
import logging

logger = logging.getLogger(__name__)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command with detailed information."""
    help_text = """
🤖 *Simple Telegram Bot - Help Guide*

*📋 Available Commands:*
/start - Show welcome message and basic info
/help - Display this detailed help guide  
/ping - Health check (responds with Pong!)

*✨ Bot Features:*
- Echo messages back to you
- Responds to all text messages instantly
- Deployed on Koyeb cloud platform
- Uses polling for reliable message delivery

*💬 How to Use:*
1. Send any of the commands above
2. Or just type any message and I'll echo it back
3. The bot is always listening and ready to respond

*🔧 Technical Info:*
- Built with python-telegram-bot library
- Running on Koyeb serverless platform
- Uses secure polling method for updates
- Handles errors gracefully with logging

*📞 Support:*
If you experience any issues, the bot logs all activities for troubleshooting.

Happy chatting! 🎉
    """
    
    await update.message.reply_text(help_text.strip(), parse_mode='Markdown')
    logger.info(f"Help command used by user: {update.effective_user.first_name}")

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /info command with bot status."""
    user = update.effective_user
    chat = update.effective_chat
    
    info_text = f"""
📊 *Bot Information*

*User Details:*
- Name: {user.first_name} {user.last_name or ''}
- Username: @{user.username or 'Not set'}
- User ID: `{user.id}`

*Chat Details:*
- Chat Type: {chat.type}
- Chat ID: `{chat.id}`

*Bot Status:*
- Status: ✅ Online and Active
- Platform: Koyeb Cloud
- Method: Polling
- Response Time: Fast

*Server Info:*
- Uptime: Running continuously
- Last Update: Just now
- Performance: Optimal
    """
    
    await update.message.reply_text(info_text.strip(), parse_mode='Markdown')
    logger.info(f"Info command used by user: {user.first_name}")

def register_help_handler(application):
    """Register help-related command handlers."""
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("info", info_command))
    logger.info("Help plugin handlers registered")
