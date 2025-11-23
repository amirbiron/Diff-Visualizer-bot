# 🚀 מדריך פריסה מהיר ברנדר

## שלב 1️⃣: קבל טוקן בוט

1. פתח את [@BotFather](https://t.me/BotFather) בטלגרם
2. שלח: `/newbot`
3. תן שם לבוט: `Diff Visualizer` (או כל שם אחר)
4. תן username: `my_diff_visualizer_bot` (חייב להסתיים ב-`bot`)
5. **שמור את הטוקן!** (נראה כך: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

## שלב 2️⃣: העלה ל-GitHub

### אם אין לך repository:

```bash
# התחל git בתיקיית הפרויקט
cd /path/to/diff-visualizer-bot
git init

# הוסף את כל הקבצים
git add .

# עשה commit ראשון
git commit -m "Initial commit: Diff Visualizer Bot"

# צור repository חדש ב-GitHub ואז:
git remote add origin https://github.com/YOUR_USERNAME/diff-visualizer-bot.git
git branch -M main
git push -u origin main
```

### אם כבר יש לך repository:

```bash
git add .
git commit -m "Add Diff Visualizer Bot"
git push
```

## שלב 3️⃣: פריסה ברנדר

### אופציה A: דרך Blueprint (הכי קל!)

1. לך ל-[Render Dashboard](https://dashboard.render.com/)
2. לחץ **"New +"** → **"Blueprint"**
3. חבר את ה-GitHub repository שלך
4. רנדר יזהה את `render.yaml` אוטומטית
5. הוסף את משתה הסביבה:
   - `TELEGRAM_BOT_TOKEN` = הטוקן שקיבלת מ-BotFather
6. לחץ **"Apply"**
7. המתן 2-3 דקות ✅

### אופציה B: Web Service רגיל

1. לך ל-[Render Dashboard](https://dashboard.render.com/)
2. לחץ **"New +"** → **"Web Service"**
3. בחר את ה-repository מ-GitHub
4. מלא את הפרטים:

   **Basic:**
   - Name: `diff-visualizer-bot`
   - Region: `Frankfurt` (או Oregon)
   - Branch: `main`
   - Root Directory: (השאר ריק)

   **Build & Deploy:**
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python diff_bot.py`

   **Plan:**
   - Instance Type: `Free` (מספיק!)

5. לחץ על **"Advanced"** ולך ל-**"Environment Variables"**
6. הוסף:
   - Key: `TELEGRAM_BOT_TOKEN`
   - Value: (הדבק את הטוקן שלך)

7. לחץ **"Create Web Service"**
8. המתן לבנייה (2-3 דקות) ✅

## שלב 4️⃣: בדיקה

1. לאחר שהסטטוס הוא **"Live"** (ירוק)
2. פתח את הבוט בטלגרם
3. שלח `/start`
4. אם הבוט עונה - **מזל טוב! 🎉**

## ⚠️ פתרון בעיות נפוצות

### הבוט לא עונה?

**בדוק Logs ברנדר:**
1. לך לדף הבוט ברנדר
2. לחץ על **"Logs"**
3. חפש שגיאות

**שגיאות נפוצות:**

```
"Unauthorized" → הטוקן לא נכון
"Module not found" → בעיה בהתקנת packages
"Connection refused" → בעיית רשת זמנית
```

**פתרונות:**
1. ודא שהטוקן נכון ב-Environment Variables
2. עשה **"Manual Deploy"** מחדש
3. בדוק ש-`requirements.txt` קיים
4. המתן כמה דקות (לפעמים לוקח זמן להתחיל)

### הבוט עובד אבל מתרסק?

בדוק את ה-Logs ותחפש:
- שגיאות Python (Traceback)
- בעיות זיכרון (Memory)
- Timeout errors

**פתרון:**
- Free tier של רנדר מספיק לרוב המקרים
- אם יש הרבה שימוש, שקול upgrade ל-Starter ($7/month)

### רוצה לעדכן את הבוט?

```bash
# עשה שינויים בקוד
git add .
git commit -m "Update bot features"
git push

# רנדר יעשה deploy אוטומטי!
```

## 🎯 טיפים נוספים

### הפעל Auto-Deploy
ברנדר → Settings → Build & Deploy → **Auto-Deploy: Yes**

עכשיו כל push ל-GitHub יעדכן אוטומטית את הבוט!

### הוסף Notifications
רנדר → Settings → Notifications → הוסף webhook/email

תקבל התראות כשיש deploy או שגיאות.

### בדוק Health
רנדר → Metrics → ראה CPU, Memory, Response Time

### Logs בזמן אמת
```bash
# אם יש לך Render CLI
render logs -f diff-visualizer-bot
```

## 🎉 סיימת!

הבוט שלך רץ 24/7 בחינם ברנדר!

**קישורים שימושיים:**
- [Render Docs](https://render.com/docs)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [python-telegram-bot Docs](https://docs.python-telegram-bot.org/)

**צריך עזרה?** פתח Issue ב-GitHub! 🤝
