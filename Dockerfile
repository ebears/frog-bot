FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Disable Python's output buffering, forwarding logs to Docker
ENV PYTHONUNBUFFERED=1

# Run the bot
CMD ["python", "bot.py"]