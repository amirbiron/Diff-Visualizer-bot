#!/usr/bin/env python3
"""
Diff Visualizer Bot - Telegram Bot for comparing code snippets
Shows beautiful colored diffs like Git
"""

import os
import logging
import difflib
from html import escape
from io import BytesIO
from typing import Optional, Tuple
from activity_reporter import create_reporter
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
    ConversationHandler
)
from telegram.constants import ParseMode

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
WAITING_FIRST, WAITING_SECOND = range(2)

# User data storage (in production, use Redis or database)
user_sessions = {}

# Activity reporting
reporter = create_reporter(
    mongodb_uri="mongodb+srv://mumin:M43M2TFgLfGvhBwY@muminai.tm6x81b.mongodb.net/?retryWrites=true&w=majority&appName=muminAI",
    service_id="srv-d4h7cqpr0fns73a2gpl0",
    service_name="Diff-Visualizer"
)


class DiffGenerator:
    """Generate beautiful colored diffs"""
    
    @staticmethod
    def generate_html_diff(text1: str, text2: str, title1: str = "Original", title2: str = "Modified") -> str:
        """Generate HTML diff with syntax highlighting"""
        
        diff = difflib.HtmlDiff(wrapcolumn=80)
        html_diff = diff.make_file(
            text1.splitlines(),
            text2.splitlines(),
            fromdesc=title1,
            todesc=title2,
            context=True,
            numlines=3
        )
        
        # Add custom CSS for better mobile viewing
        custom_css = """
        <style>
            /* 1. הגדרות בסיס: פונט קוד ורקע כהה */
            body { 
                background: #1e1e1e; 
                color: #d4d4d4; 
                font-family: Consolas, 'Courier New', monospace; /* קריטי ליישור */
                padding: 10px;
            }
            
            /* 2. צבעים בסגנון VS Code (נעימים יותר לעין) */
            .diff_add { background: #203622; color: #b4eebb; } /* ירוק */
            .diff_sub { background: #421818; color: #ffaaaa; } /* אדום */
            .diff_chg { background: #3e3e15; color: #ffffb3; } /* צהוב */

            /* 3. התיקון הקריטי לעברית וסוגריים */
            table.diff { 
                width: 100%; 
                direction: ltr; /* מגדיר את כיוון הטבלה כולה */
                border-collapse: collapse;
            }
            
            td { 
                direction: ltr !important;    /* מכריח את השורה להתנהג כאנגלית */
                text-align: left !important;  /* מצמיד הכל לשמאל */
                unicode-bidi: isolate;        /* הקסם: מבודד את העברית כדי שלא תהפוך את הפיסוק */
                white-space: pre-wrap;        /* שומר על רווחים ואינדנטציה במדויק */
                padding: 2px 5px;             /* קצת מרווח לנשימה */
            }
            
            /* הגנה נוספת לאלמנטים פנימיים (מספרים בתוך עברית) */
            span { unicode-bidi: isolate; }
            
            /* הסתרת המקרא המיושן למעלה (אופציונלי) */
            .diff_header { display: none; }
        </style>
        """
        
        # Inject custom CSS
        html_diff = html_diff.replace('</head>', custom_css + '</head>')
        
        return html_diff
    
    @staticmethod
    def generate_text_diff(text1: str, text2: str) -> str:
        """Generate simple text diff for Telegram message"""
        
        lines1 = text1.splitlines()
        lines2 = text2.splitlines()
        
        diff = list(difflib.unified_diff(
            lines1, 
            lines2, 
            lineterm='',
            fromfile='Original',
            tofile='Modified'
        ))
        
        if not diff:
            return "✅ הקבצים זהים לחלוטין!"
        
        # Format for Telegram
        formatted_diff = []
        stats = {'added': 0, 'removed': 0, 'changed': 0}
        
        for line in diff:
            if line.startswith('+++') or line.startswith('---'):
                formatted_diff.append(f"📄 {line}")
            elif line.startswith('@@'):
                formatted_diff.append(f"\n📍 {line}")
            elif line.startswith('+'):
                formatted_diff.append(f"➕ {line[1:]}")
                stats['added'] += 1
            elif line.startswith('-'):
                formatted_diff.append(f"➖ {line[1:]}")
                stats['removed'] += 1
            elif line.startswith('?'):
                continue  # Skip hint lines
            else:
                formatted_diff.append(f"   {line}")
        
        # Add statistics
        stats_text = f"\n\n📊 סטטיסטיקה:\n"
        stats_text += f"➕ נוספו: {stats['added']} שורות\n"
        stats_text += f"➖ הוסרו: {stats['removed']} שורות\n"
        
        result = '\n'.join(formatted_diff[:50])  # Limit for Telegram
        
        if len(formatted_diff) > 50:
            result += f"\n\n⚠️ ... ועוד {len(formatted_diff) - 50} שורות"
        
        return result + stats_text


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcome message"""
    
    reporter.report_activity(update.effective_user.id)

    welcome_text = """
🎨 <b>ברוכים הבאים ל-Diff Visualizer Bot!</b>

בוט זה מאפשר לך להשוות בין שני קטעי קוד ולקבל תצוגת Diff צבעונית כמו ב-Git.

<b>איך להשתמש:</b>
1️⃣ שלח את קטע הקוד הראשון (Original)
2️⃣ שלח את קטע הקוד השני (Modified)
3️⃣ קבל Diff מפורט עם הבדלים מסומנים!

<b>פקודות זמינות:</b>
/start - הצג הודעה זו
/new - התחל השוואה חדשה
/help - עזרה ומידע נוסף
/example - דוגמה מהירה

💡 <b>טיפ:</b> אפשר לשלוח קוד כטקסט רגיל או כקובץ!
    """
    
    keyboard = [
        [InlineKeyboardButton("🆕 התחל השוואה חדשה", callback_data='new_comparison')],
        [InlineKeyboardButton("📖 דוגמה", callback_data='show_example')],
        [InlineKeyboardButton("❓ עזרה", callback_data='show_help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_text,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup
    )


async def new_comparison(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start new comparison"""
    
    reporter.report_activity(update.effective_user.id)

    user_id = update.effective_user.id
    
    # Clear previous session
    user_sessions[user_id] = {
        'first_code': None,
        'second_code': None,
        'first_name': 'Original',
        'second_name': 'Modified'
    }
    
    message = "📝 <b>השוואה חדשה</b>\n\n"
    message += "שלח את קטע הקוד הראשון (Original):\n"
    message += "• אפשר לשלוח כטקסט רגיל\n"
    message += "• אפשר לשלוח כקובץ (.txt, .py, .js וכו')\n\n"
    message += "לביטול: /cancel"
    
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.reply_text(
            message,
            parse_mode=ParseMode.HTML
        )
    else:
        await update.message.reply_text(
            message,
            parse_mode=ParseMode.HTML
        )
    
    return WAITING_FIRST


async def receive_first_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Receive first code snippet"""
    
    reporter.report_activity(update.effective_user.id)

    user_id = update.effective_user.id
    
    # Get code from message or document
    if update.message.document:
        # Handle file upload
        file = await update.message.document.get_file()
        file_content = await file.download_as_bytearray()
        code = file_content.decode('utf-8', errors='ignore')
        filename = update.message.document.file_name
        user_sessions[user_id]['first_name'] = filename
    elif update.message.text:
        code = update.message.text
    else:
        await update.message.reply_text("❌ סוג קובץ לא נתמך. שלח טקסט או קובץ.")
        return WAITING_FIRST
    
    user_sessions[user_id]['first_code'] = code
    
    message = f"✅ קוד ראשון נשמר ({len(code)} תווים)\n\n"
    message += "📝 עכשיו שלח את קטע הקוד השני (Modified):\n"
    message += "לביטול: /cancel"
    
    await update.message.reply_text(message)
    
    return WAITING_SECOND


async def receive_second_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Receive second code snippet and generate diff"""
    
    reporter.report_activity(update.effective_user.id)

    user_id = update.effective_user.id
    
    # Get code from message or document
    if update.message.document:
        file = await update.message.document.get_file()
        file_content = await file.download_as_bytearray()
        code = file_content.decode('utf-8', errors='ignore')
        filename = update.message.document.file_name
        user_sessions[user_id]['second_name'] = filename
    elif update.message.text:
        code = update.message.text
    else:
        await update.message.reply_text("❌ סוג קובץ לא נתמך. שלח טקסט או קובץ.")
        return WAITING_SECOND
    
    user_sessions[user_id]['second_code'] = code
    
    # Generate diff
    await update.message.reply_text("⏳ מייצר Diff...")
    
    session = user_sessions[user_id]
    diff_gen = DiffGenerator()
    
    # Generate text diff for preview
    text_diff = diff_gen.generate_text_diff(
        session['first_code'],
        session['second_code']
    )
    
    # Prepare safe preview text for Telegram (HTML)
    preview_limit = 2500
    is_truncated = len(text_diff) > preview_limit
    preview_text = text_diff[:preview_limit]
    escaped_preview = escape(preview_text)
    
    preview_message = (
        "<b>🔍 תצוגת Diff מקדימה</b>\n\n"
        f"<pre>{escaped_preview}</pre>"
    )
    
    if is_truncated:
        preview_message += (
            "\n⚠️ התצוגה קוצרה עבור טלגרם. "
            "לקבלת כל ההבדלים לחץ על קובץ ה-HTML."
        )
    
    keyboard = [
        [InlineKeyboardButton("📄 קבל קובץ HTML מלא", callback_data='get_html_diff')],
        [InlineKeyboardButton("🔄 השוואה חדשה", callback_data='new_comparison')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        preview_message,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup
    )
    
    return ConversationHandler.END


async def send_html_diff(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send HTML diff file"""
    
    reporter.report_activity(update.effective_user.id)

    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if user_id not in user_sessions or not user_sessions[user_id]['first_code']:
        await query.message.reply_text("❌ אין נתונים. התחל השוואה חדשה עם /new")
        return
    
    session = user_sessions[user_id]
    diff_gen = DiffGenerator()
    
    # Generate HTML diff
    html_diff = diff_gen.generate_html_diff(
        session['first_code'],
        session['second_code'],
        session['first_name'],
        session['second_name']
    )
    
    # Create file
    html_bytes = html_diff.encode('utf-8')
    bio = BytesIO(html_bytes)
    bio.name = 'diff_visualization.html'
    
    await query.message.reply_document(
        document=bio,
        filename='diff_visualization.html',
        caption="📄 קובץ HTML עם תצוגת Diff מלאה\nפתח בדפדפן לתצוגה אופטימלית!"
    )


async def show_example(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show usage example"""
    
    reporter.report_activity(update.effective_user.id)

    query = update.callback_query
    await query.answer()
    
    example_text = """
<b>📖 דוגמה לשימוש</b>

<b>קוד מקורי:</b>
<pre>def hello():
    print("Hello World")
    return True</pre>

<b>קוד מעודכן:</b>
<pre>def hello(name):
    print(f"Hello {name}")
    return True</pre>

<b>התוצאה תהיה:</b>
➕ שורות שנוספו (ירוק)
➖ שורות שהוסרו (אדום)
📍 מיקום השינויים

<b>רוצה לנסות?</b> לחץ על "התחל השוואה חדשה" 👇
    """
    
    keyboard = [
        [InlineKeyboardButton("🆕 התחל השוואה חדשה", callback_data='new_comparison')],
        [InlineKeyboardButton("🔙 חזרה", callback_data='back_to_start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.edit_text(
        example_text,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup
    )


async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show help information"""
    
    reporter.report_activity(update.effective_user.id)

    query = update.callback_query
    await query.answer()
    
    help_text = """
<b>❓ עזרה - Diff Visualizer Bot</b>

<b>מה הבוט עושה?</b>
הבוט משווה בין שני קטעי קוד ומציג את ההבדלים בצורה ויזואלית, בדיוק כמו Git diff.

<b>איך זה עובד?</b>
1. שלח קטע קוד ראשון
2. שלח קטע קוד שני
3. קבל השוואה מפורטת!

<b>פורמטים נתמכים:</b>
✅ טקסט רגיל
✅ קבצי קוד (.py, .js, .java, .cpp וכו')
✅ קבצי טקסט (.txt, .md)

<b>תצוגות זמינות:</b>
• תצוגת טקסט - מהירה ונוחה
• קובץ HTML - עם צבעים וסינטקס מלא

<b>פקודות:</b>
/start - תפריט ראשי
/new - השוואה חדשה
/cancel - ביטול
/help - עזרה זו

<b>💡 טיפים:</b>
• הבוט שומר את ההשוואה האחרונה
• אפשר להוריד HTML לשמירה
• עובד מעולה עם כל שפת תכנות
    """
    
    keyboard = [
        [InlineKeyboardButton("🔙 חזרה", callback_data='back_to_start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.edit_text(
        help_text,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup
    )


async def back_to_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Return to start menu"""
    
    reporter.report_activity(update.effective_user.id)

    query = update.callback_query
    await query.answer()
    
    welcome_text = """
🎨 <b>Diff Visualizer Bot</b>

השווה בין שני קטעי קוד וקבל תצוגת Diff צבעונית!

בחר פעולה מהתפריט למטה:
    """
    
    keyboard = [
        [InlineKeyboardButton("🆕 התחל השוואה חדשה", callback_data='new_comparison')],
        [InlineKeyboardButton("📖 דוגמה", callback_data='show_example')],
        [InlineKeyboardButton("❓ עזרה", callback_data='show_help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.edit_text(
        welcome_text,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup
    )


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel current operation"""
    
    reporter.report_activity(update.effective_user.id)

    user_id = update.effective_user.id
    if user_id in user_sessions:
        del user_sessions[user_id]
    
    await update.message.reply_text(
        "❌ הפעולה בוטלה.\n\nלהתחלת השוואה חדשה: /new"
    )
    
    return ConversationHandler.END


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle button callbacks"""
    
    reporter.report_activity(update.effective_user.id)

    query = update.callback_query
    
    if query.data == 'new_comparison':
        return await new_comparison(update, context)
    elif query.data == 'get_html_diff':
        await send_html_diff(update, context)
    elif query.data == 'show_example':
        await show_example(update, context)
    elif query.data == 'show_help':
        await show_help(update, context)
    elif query.data == 'back_to_start':
        await back_to_start(update, context)
    
    return ConversationHandler.END


def main() -> None:
    """Start the bot"""
    
    # Get token from environment
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set!")
    
    # Create application
    application = Application.builder().token(token).build()
    
    # Conversation handler
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('new', new_comparison),
            CallbackQueryHandler(button_handler, pattern='^new_comparison$')
        ],
        states={
            WAITING_FIRST: [
                MessageHandler(filters.TEXT | filters.Document.ALL, receive_first_code)
            ],
            WAITING_SECOND: [
                MessageHandler(filters.TEXT | filters.Document.ALL, receive_second_code)
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    
    # Add handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', lambda u, c: show_help(u, c) if u.callback_query else None))
    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Start bot
    logger.info("🚀 Diff Visualizer Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
