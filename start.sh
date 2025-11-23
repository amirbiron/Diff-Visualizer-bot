#!/bin/bash

# Quick Start Script for Diff Visualizer Bot
# הסקריפט הזה עוזר להריץ את הבוט במהירות

echo "🎨 Diff Visualizer Bot - Quick Start"
echo "===================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  קובץ .env לא נמצא!"
    echo "📝 יוצר .env מתבנית..."
    cp .env.example .env
    echo ""
    echo "✅ קובץ .env נוצר!"
    echo "📌 אנא ערוך את הקובץ .env והכנס את הטוקן שלך:"
    echo "   TELEGRAM_BOT_TOKEN=your_bot_token_here"
    echo ""
    echo "💡 לאחר מכן הרץ שוב סקריפט זה"
    exit 1
fi

# Check if token is set
source .env
if [ -z "$TELEGRAM_BOT_TOKEN" ] || [ "$TELEGRAM_BOT_TOKEN" = "your_bot_token_here" ]; then
    echo "❌ טוקן לא הוגדר ב-.env"
    echo "📝 ערוך את .env והכנס את הטוקן שלך"
    exit 1
fi

echo "✅ קובץ .env נמצא!"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 יוצר virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment נוצר!"
    echo ""
fi

# Activate virtual environment
echo "🔌 מפעיל virtual environment..."
source venv/bin/activate
echo ""

# Install dependencies
echo "📥 מתקין תלויות..."
pip install -r requirements.txt --quiet
echo "✅ תלויות הותקנו!"
echo ""

# Run the bot
echo "🚀 מפעיל את הבוט..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

python diff_bot.py
