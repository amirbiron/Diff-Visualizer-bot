# 🔍 Diff Visualizer Bot

בוט טלגרם שמציג השוואה צבעונית בין שני קטעי קוד, בדיוק כמו ב-Git!

## 🚀 התקנה ב-Render

### שלב 1: יצירת בוט בטלגרם
1. פתח שיחה עם [@BotFather](https://t.me/botfather) בטלגרם
2. שלח `/newbot` וצור בוט חדש
3. שמור את ה-Token שתקבל

### שלב 2: העלאה ל-Render
1. צור חשבון ב-[Render.com](https://render.com)
2. לחץ על **New +** ובחר **Web Service**
3. חבר את המאגר שלך מ-GitHub/GitLab או העלה את הקבצים
4. הגדרות:
   - **Name**: `diff-visualizer-bot`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python diff_bot.py`
5. לחץ על **Environment** והוסף משתנה:
   - **Key**: `TELEGRAM_BOT_TOKEN`
   - **Value**: (ה-Token מ-BotFather)
6. לחץ על **Create Web Service**

### שלב 3: שימוש בבוט
1. פתח את הבוט בטלגרם (הלינק שקיבלת מ-BotFather)
2. שלח `/start` לקבלת הוראות
3. שלח `/diff` להתחלת השוואה
4. שלח את קטע הקוד הראשון
5. שלח את קטע הקוד השני
6. קבל תצוגת Diff צבעונית!

## 📋 פקודות

- `/start` - הצגת הוראות שימוש
- `/diff` - התחלת השוואה חדשה
- `/cancel` - ביטול פעולה נוכחית

## 🎨 תכונות

✅ תצוגת Diff צבעונית עם אמוג'ים  
✅ תמיכה בכל שפות התכנות  
✅ סימון שורות שנוספו (➕) ושנמחקו (➖)  
✅ תצוגה ברורה כמו Git  
✅ ממשק עברית ידידותי  

## 📁 מבנה הפרויקט

```
.
├── diff_bot.py          # קוד הבוט
├── requirements.txt     # תלויות Python
└── README.md           # קובץ זה
```

## 🛠️ טכנולוגיות

- Python 3.11+
- python-telegram-bot 22.5 (תואם ל-Python 3.13)
- difflib (מובנה ב-Python)
- Render.com (הוסטינג)

## 💡 דוגמת שימוש

```
משתמש: /diff
בוט: 📋 שלח את קטע הקוד הראשון

משתמש: 
def hello():
    print("Hello")

בוט: ✅ קוד ראשון התקבל! עכשיו שלח את קטע הקוד השני

משתמש:
def hello():
    print("Hello World!")

בוט: 
🔍 תוצאת ההשוואה:

🔹 @@ -1,2 +1,2 @@
  def hello():
➖     print("Hello")
➕     print("Hello World!")
```

## 🐛 בעיות נפוצות

### הבוט לא עונה
- ודא ש-Render Service פעיל (לא Suspended)
- בדוק שה-TELEGRAM_BOT_TOKEN נכון ב-Environment Variables
- בדוק לוגים ב-Render Dashboard

### שגיאות בהתקנה
- ודא שקובץ requirements.txt קיים
- ודא ש-Python version הוא 3.11 או חדש יותר
- אם מופיעה שגיאת `AttributeError: 'Updater' object has no attribute '_Updater__polling_cleanup_cb'`, ודא שהתקנת את התלויות מחדש (`pip install -r requirements.txt`). הגרסה המעודכנת של python-telegram-bot פותרת את הבעיה ב-Python 3.13.

## 📝 הערות

- Render מציע Free Tier שמספיק לבוט קטן
- הבוט יכבה אחרי 15 דקות של חוסר פעילות ב-Free Tier
- אפשר לשדרג לתוכנית בתשלום לפעילות 24/7

## 📞 תמיכה

יש בעיה? צור קשר או פתח Issue במאגר הקוד.

---

נוצר עם ❤️ בעזרת Python ו-Telegram Bot API
