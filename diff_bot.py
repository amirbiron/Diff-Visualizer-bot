import os
import difflib
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# States for conversation
WAITING_FIRST_CODE, WAITING_SECOND_CODE = range(2)

# Bot token from environment variable
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command - explain how to use the bot"""
    welcome_message = (
        "👋 ברוך הבא ל-Diff Visualizer Bot!\n\n"
        "🔍 הבוט הזה מציג השוואה צבעונית בין שני קטעי קוד, בדיוק כמו ב-Git.\n\n"
        "📝 איך להשתמש:\n"
        "1. שלח /diff להתחלת השוואה חדשה\n"
        "2. שלח את קטע הקוד הראשון (הגרסה הישנה)\n"
        "3. שלח את קטע הקוד השני (הגרסה החדשה)\n"
        "4. קבל תצוגת Diff מעוצבת!\n\n"
        "💡 הבוט תומך בכל שפת תכנות ומדגיש הבדלים בצבעים."
    )
    await update.message.reply_text(welcome_message)

async def diff_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the diff comparison process"""
    await update.message.reply_text(
        "📋 שלח את קטע הקוד הראשון (הגרסה הישנה):",
        reply_markup=ForceReply(selective=True)
    )
    return WAITING_FIRST_CODE

async def receive_first_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive the first code snippet"""
    context.user_data['first_code'] = update.message.text
    await update.message.reply_text(
        "✅ קוד ראשון התקבל!\n\n📋 עכשיו שלח את קטע הקוד השני (הגרסה החדשה):",
        reply_markup=ForceReply(selective=True)
    )
    return WAITING_SECOND_CODE

async def receive_second_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive the second code snippet and generate diff"""
    first_code = context.user_data.get('first_code', '')
    second_code = update.message.text
    
    # Generate diff
    diff_result = generate_diff(first_code, second_code)
    
    # Send the diff result
    await update.message.reply_text(
        "🔍 תוצאת ההשוואה:\n\n" + diff_result,
        parse_mode='HTML'
    )
    
    await update.message.reply_text(
        "✨ רוצה להשוות עוד? שלח /diff",
    )
    
    # Clear user data
    context.user_data.clear()
    return ConversationHandler.END

def generate_diff(old_code: str, new_code: str) -> str:
    """Generate a colored diff between two code snippets"""
    old_lines = old_code.splitlines(keepends=True)
    new_lines = new_code.splitlines(keepends=True)
    
    # Generate unified diff
    diff = difflib.unified_diff(
        old_lines, 
        new_lines, 
        fromfile='Old Version', 
        tofile='New Version',
        lineterm=''
    )
    
    # Format diff with HTML and emojis
    result = []
    result.append("<pre>")
    
    for line in diff:
        line = line.rstrip()
        if line.startswith('+++') or line.startswith('---'):
            # File headers
            result.append(f"<b>{escape_html(line)}</b>")
        elif line.startswith('@@'):
            # Hunk header
            result.append(f"<b>🔹 {escape_html(line)}</b>")
        elif line.startswith('+'):
            # Added line
            result.append(f"<b>➕ {escape_html(line)}</b>")
        elif line.startswith('-'):
            # Removed line
            result.append(f"<b>➖ {escape_html(line)}</b>")
        else:
            # Context line
            result.append(f"  {escape_html(line)}")
    
    result.append("</pre>")
    
    if len(result) <= 2:  # Only pre tags, no actual diff
        return "✅ הקודים זהים! לא נמצאו הבדלים."
    
    return '\n'.join(result)

def escape_html(text: str) -> str:
    """Escape HTML special characters"""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the current operation"""
    context.user_data.clear()
    await update.message.reply_text(
        "❌ פעולה בוטלה. שלח /diff להתחלה מחדש."
    )
    return ConversationHandler.END

def main():
    """Start the bot"""
    if not TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN environment variable not set!")
        return
    
    # Create application
    application = Application.builder().token(TOKEN).build()
    
    # Conversation handler for diff flow
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('diff', diff_command)],
        states={
            WAITING_FIRST_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_first_code)],
            WAITING_SECOND_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_second_code)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    
    # Add handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(conv_handler)
    
    # Start the bot
    print("🤖 Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
