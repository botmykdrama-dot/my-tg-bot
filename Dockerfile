FROM python:3.11-slim

WORKDIR /app

# Install dependencies first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot code
COPY bot.py .

# Expose port
EXPOSE 8080

# Run the bot (important: -u for unbuffered output)
CMD ["python", "-u", "bot.py"]
