echo "🚀 Deploying Sinhala OCR Bot to Koyeb..."

# Check if Koyeb CLI is installed
if ! command -v koyeb &> /dev/null; then
    echo "❌ Koyeb CLI not found. Please install it first:"
    echo "curl -fsSL https://koyeb.com/install.sh | bash"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please create it from .env.example"
    exit 1
fi

# Load environment variables
export $(grep -v '^#' .env | xargs)

# Check if bot token is set
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "❌ TELEGRAM_BOT_TOKEN not set in .env file"
    exit 1
fi

echo "✅ Environment variables loaded"

# Deploy to Koyeb
echo "📦 Deploying to Koyeb..."
koyeb app deploy sinhala-ocr-bot \
    --git https://github.com/yourusername/sinhala-ocr-bot \
    --git-branch main \
    --instance-type nano \
    --env TELEGRAM_BOT_TOKEN="$TELEGRAM_BOT_TOKEN" \
    --port 8000

echo "✅ Deployment initiated!"
echo "🔗 Check your deployment status at: https://app.koyeb.com"
