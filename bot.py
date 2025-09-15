import logging
import os
import io
import cv2
import numpy as np
from PIL import Image
import easyocr
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import asyncio
import signal
import sys
from threading import Thread
import time

# Enable logging with cloud-friendly format
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

class SinhalaOCRBot:
    def __init__(self, bot_token):
        self.bot_token = bot_token
        self.reader = None
        self.application = None
        self._initialize_ocr()
        
    def _initialize_ocr(self):
        """Initialize EasyOCR reader with error handling."""
        try:
            logger.info("Initializing EasyOCR reader...")
            # Initialize with CPU only for cloud deployment
            self.reader = easyocr.Reader(['si', 'en'], gpu=False, verbose=False)
            logger.info("EasyOCR reader initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize EasyOCR: {e}")
            raise
        
    async def start(self, update: Update, context: CallbackContext):
        """Send a message when the command /start is issued."""
        welcome_message = """
🙏 සුභ උදෑසනක්! Welcome to Sinhala Handwriting Recognition Bot!

📝 Send me an image with handwritten Sinhala text and I'll convert it to digital text.

🔹 Supported formats: JPG, PNG, WebP
🔹 For best results:
   • Use clear, well-lit images
   • Ensure text is clearly visible
   • Avoid blurry or distorted images

Commands:
/start - Show this welcome message
/help - Get help and tips
/about - About this bot
/status - Check bot status

Just send me an image to get started! 📸
        """
        await update.message.reply_text(welcome_message)

    async def help_command(self, update: Update, context: CallbackContext):
        """Send help message with tips for better recognition."""
        help_text = """
📋 Tips for Better Recognition:

✅ Image Quality:
   • Use good lighting
   • Keep the camera steady
   • Ensure text fills most of the image

✅ Handwriting Tips:
   • Write clearly and neatly
   • Use dark ink on light paper
   • Avoid overlapping characters
   • Leave space between words

✅ Technical:
   • Supported formats: JPG, PNG, WebP
   • Maximum file size: 20MB
   • Both Sinhala and English text supported

🔄 If recognition fails, try:
   • Taking a clearer photo
   • Adjusting lighting
   • Cropping to focus on text only

Need more help? Contact the developer! 💬
        """
        await update.message.reply_text(help_text)

    async def about(self, update: Update, context: CallbackContext):
        """Send information about the bot."""
        about_text = """
🤖 Sinhala Handwriting Recognition Bot

This bot uses advanced OCR technology to recognize handwritten Sinhala text from images.

🔧 Technology Stack:
   • EasyOCR for text recognition
   • OpenCV for image processing
   • Python Telegram Bot API
   • Deployed on Koyeb Cloud

🌟 Features:
   • Sinhala script recognition
   • English text support
   • Image preprocessing
   • High accuracy OCR

Made with ❤️ for the Sinhala community
Deployed on Koyeb for 24/7 availability
        """
        await update.message.reply_text(about_text)

    async def status(self, update: Update, context: CallbackContext):
        """Check bot status."""
        status_text = f"""
🟢 Bot Status: Online

🔧 System Info:
   • OCR Engine: {'Ready' if self.reader else 'Not Ready'}
   • Memory Usage: Available
   • Cloud Platform: Koyeb
   • Uptime: Active

✅ All systems operational!
        """
        await update.message.reply_text(status_text)

    def preprocess_image(self, image):
        """Preprocess the image for better OCR results."""
        try:
            # Convert to grayscale
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image.copy()
            
            # Apply Gaussian blur to reduce noise
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Apply adaptive thresholding
            thresh = cv2.adaptiveThreshold(
                blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY, 11, 2
            )
            
            # Morphological operations to clean up the image
            kernel = np.ones((2, 2), np.uint8)
            cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            
            return cleaned
        except Exception as e:
            logger.error(f"Image preprocessing error: {e}")
            return image

    async def process_image(self, update: Update, context: CallbackContext):
        """Process the received image and extract Sinhala text."""
        if not self.reader:
            await update.message.reply_text("❌ OCR engine not ready. Please try again later.")
            return
            
        try:
            # Send processing message
            processing_msg = await update.message.reply_text("🔄 Processing your image... Please wait.")
            
            # Get the largest photo size
            photo = update.message.photo[-1]
            
            # Download the image with timeout
            file = await context.bot.get_file(photo.file_id)
            image_bytes = io.BytesIO()
            await file.download_to_memory(image_bytes)
            image_bytes.seek(0)
            
            # Convert to OpenCV format
            pil_image = Image.open(image_bytes)
            opencv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            
            # Preprocess the image
            processed_image = self.preprocess_image(opencv_image)
            
            # Perform OCR with timeout handling
            results = self.reader.readtext(processed_image)
            
            # Extract text
            extracted_text = []
            confidence_scores = []
            
            for (bbox, text, confidence) in results:
                if confidence > 0.3:  # Filter out low-confidence results
                    extracted_text.append(text.strip())
                    confidence_scores.append(confidence)
            
            # Delete processing message
            await processing_msg.delete()
            
            if extracted_text:
                # Format the response
                recognized_text = "\n".join(extracted_text)
                avg_confidence = np.mean(confidence_scores) if confidence_scores else 0
                
                response = f"""
📝 Recognized Text:

{recognized_text}

📊 Confidence: {avg_confidence:.1%}
🔢 Words found: {len(extracted_text)}

💡 Tip: If the result isn't accurate, try taking a clearer photo with better lighting!
                """
                
                await update.message.reply_text(response)
                
                # Log successful recognition
                logger.info(f"Successfully recognized text for user {update.effective_user.id}")
                
            else:
                await update.message.reply_text("""
❌ No text could be recognized in this image.

Try these tips:
• Ensure the handwriting is clear and legible
• Use better lighting
• Make sure the text is large enough
• Check if the image is not blurry

Send another image to try again! 📸
                """)
                
        except Exception as e:
            logger.error(f"Error processing image: {e}")
            try:
                await processing_msg.delete()
            except:
                pass
            await update.message.reply_text("""
⚠️ Sorry, there was an error processing your image.

This could be due to:
• Unsupported image format
• Image too large or corrupted
• Temporary server issue

Please try again with a different image! 🔄
            """)

    async def handle_non_image(self, update: Update, context: CallbackContext):
        """Handle non-image messages."""
        await update.message.reply_text("""
📸 Please send me an image with handwritten Sinhala text!

Supported formats: JPG, PNG, WebP

Use /help for tips on getting better recognition results.
        """)

    def setup_handlers(self):
        """Setup bot handlers."""
        # Create application
        self.application = Application.builder().token(self.bot_token).build()
        
        # Add handlers
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("about", self.about))
        self.application.add_handler(CommandHandler("status", self.status))
        
        # Handle images
        self.application.add_handler(MessageHandler(filters.PHOTO, self.process_image))
        
        # Handle non-image messages
        self.application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND, self.handle_non_image
        ))
        self.application.add_handler(MessageHandler(
            filters.Document.ALL | filters.AUDIO | filters.VIDEO | filters.VOICE,
            self.handle_non_image
        ))

    async def start_bot(self):
        """Start the bot with proper initialization."""
        logger.info("Starting Sinhala OCR Bot...")
        
        # Initialize the application
        await self.application.initialize()
        await self.application.start()
        
        # Start polling
        await self.application.updater.start_polling()
        
        logger.info("Bot is running...")
        
        # Keep the bot running
        try:
            while True:
                await asyncio.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            logger.info("Stopping bot...")
        finally:
            await self.application.stop()

    def run(self):
        """Run the bot with proper async handling."""
        self.setup_handlers()
        
        # Handle graceful shutdown
        def signal_handler(signum, frame):
            logger.info("Received shutdown signal")
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Run the async bot
        try:
            asyncio.run(self.start_bot())
        except Exception as e:
            logger.error(f"Bot encountered an error: {e}")

def main():
    """Main function to run the bot."""
    # Get bot token from environment variable
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN environment variable not set!")
        sys.exit(1)
    
    # Create and run the bot
    bot = SinhalaOCRBot(BOT_TOKEN)
    bot.run()

if __name__ == '__main__':
    main()
