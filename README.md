# 🎨 Diff Visualizer Bot

בוט טלגרם להשוואת קוד עם תצוגת Diff צבעונית כמו Git.

## ✨ תכונות

- 📊 השוואה ויזואלית בין שני קטעי קוד
- 🎨 תצוגת Diff צבעונית (HTML + טקסט)
- 📁 תמיכה בקבצים וטקסט חופשי
- 📈 סטטיסטיקות על שינויים
- 🌐 ממשק בעברית
- 🚀 קל לפריסה ברנדר

## 🚀 התקנה מקומית

### דרישות מוקדמות

- Python 3.9+
- טוקן בוט טלגרם (מ-@BotFather)

### שלבי התקנה

1. **שכפול/הורדת הקוד**
```bash
# אם יש לך git
git clone <repository-url>
cd diff-visualizer-bot

# או פשוט העתק את הקבצים לתיקייה
```

2. **התקנת תלויות**
```bash
pip install -r requirements.txt
```

3. **הגדרת משתני סביבה**
```bash
# העתק את הקובץ לדוגמה
cp .env.example .env

# ערוך את .env והכנס את הטוקן שלך
TELEGRAM_BOT_TOKEN=your_actual_bot_token_here
```

4. **הרצת הבוט**
```bash
python diff_bot.py
```

## 🌐 פריסה ברנדר (Render)

### שלב 1: יצירת בוט טלגרם

1. פתח שיחה עם [@BotFather](https://t.me/BotFather) בטלגרם
2. שלח: `/newbot`
3. בחר שם לבוט (למשל: "My Diff Visualizer")
4. בחר username (חייב להסתיים ב-bot, למשל: `my_diff_bot`)
5. שמור את הטוקן שתקבל!

### שלב 2: העלאה לרנדר

#### אופציה 1: דרך GitHub (מומלץ)

1. **צור repository חדש ב-GitHub**
   - לך ל-[GitHub](https://github.com/new)
   - צור repository חדש (פרטי או ציבורי)

2. **העלה את הקבצים**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Diff Visualizer Bot"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

3. **פריסה ברנדר**
   - לך ל-[Render Dashboard](https://dashboard.render.com/)
   - לחץ "New +" → "Web Service"
   - חבר את ה-GitHub repository
   - מלא את הפרטים:
     - **Name**: `diff-visualizer-bot`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python diff_bot.py`
     - **Instance Type**: `Free`

4. **הוסף משתני סביבה**
   - בעמוד ההגדרות, לך ל-"Environment"
   - הוסף:
     - Key: `TELEGRAM_BOT_TOKEN`
     - Value: הטוקן שקיבלת מ-BotFather

5. **Deploy!**
   - לחץ "Create Web Service"
   - המתן להשלמת הבנייה (2-3 דקות)

#### אופציה 2: ללא GitHub

אם אין לך GitHub, צור קובץ `render.yaml`:

```yaml
services:
  - type: web
    name: diff-visualizer-bot
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python diff_bot.py
    envVars:
      - key: TELEGRAM_BOT_TOKEN
        sync: false
```

ואז העלה ידנית דרך Render Dashboard.

## 📖 איך להשתמש

1. **פתח את הבוט** - חפש את הבוט בטלגרם
2. **שלח** `/start` להתחלה
3. **לחץ** "התחל השוואה חדשה"
4. **שלח** את קטע הקוד הראשון
5. **שלח** את קטע הקוד השני
6. **קבל** תצוגת Diff מפורטת!

### דוגמה מהירה

**קוד 1:**
```python
def hello():
    print("Hello World")
```

**קוד 2:**
```python
def hello(name):
    print(f"Hello {name}!")
```

**תוצאה:**
```
➖ def hello():
➕ def hello(name):
➖     print("Hello World")
➕     print(f"Hello {name}!")
```

## 🎯 פקודות זמינות

- `/start` - התחלת הבוט והצגת תפריט
- `/new` - התחלת השוואה חדשה
- `/help` - הצגת עזרה
- `/cancel` - ביטול פעולה נוכחית

## 🛠️ פיצ'רים מתקדמים

### תצוגות שונות
- **תצוגת טקסט** - מהירה, ישירות בטלגרם
- **קובץ HTML** - עם צבעים מלאים וסינטקס הייליטינג

### תמיכה בקבצים
הבוט תומך ב:
- `.py`, `.js`, `.java`, `.cpp`, `.c`, `.cs`
- `.html`, `.css`, `.scss`
- `.json`, `.xml`, `.yaml`
- `.txt`, `.md`
- וכל קובץ טקסט אחר!

### סטטיסטיקות
הבוט מציג:
- מספר שורות שנוספו
- מספר שורות שהוסרו
- מיקום השינויים

## 🔧 אפשרויות נוספות

### הרצה עם Docker (אופציונלי)

צור `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY diff_bot.py .

CMD ["python", "diff_bot.py"]
```

הרצה:
```bash
docker build -t diff-bot .
docker run -e TELEGRAM_BOT_TOKEN=your_token diff-bot
```

### Webhook במקום Polling (לפרודקשן)

אפשר להוסיף תמיכה ב-webhooks להרצה יעילה יותר:

```python
# במקום run_polling, השתמש ב:
application.run_webhook(
    listen="0.0.0.0",
    port=int(os.environ.get('PORT', 10000)),
    url_path=token,
    webhook_url=f"{os.environ.get('WEBHOOK_URL')}/{token}"
)
```

## 🐛 פתרון בעיות

### הבוט לא עונה
1. בדוק שהטוקן נכון ב-`.env` או במשתני הסביבה ברנדר
2. ודא שהשירות ברנדר רץ (Status: Live)
3. בדוק את ה-Logs ברנדר

### שגיאות בקוד
- ודא ש-Python 3.9+ מותקן
- התקן מחדש את התלויות: `pip install -r requirements.txt`
- בדוק את ה-Logs לפרטים

### בעיות ברנדר
- ודא שה-Build Command נכון
- בדוק שיש משתה סביבה `TELEGRAM_BOT_TOKEN`
- לפעמים צריך לעשות "Manual Deploy" מחדש

## 📝 רישיון

פרויקט זה בקוד פתוח ללא רישיון ספציפי.
אתה מוזמן להשתמש, לשנות ולשתף!

## 🤝 תרומה

רוצה לשפר את הבוט?
- פתח Issue
- שלח Pull Request
- שתף רעיונות!

## 📧 יצירת קשר

נתקלת בבעיה או יש לך שאלות? פתח Issue ב-GitHub!

---

**נוצר עם ❤️ לקהילת המפתחים העבריים**
