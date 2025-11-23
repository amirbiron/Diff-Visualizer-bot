# 🚀 התחלה מהירה - Diff Visualizer Bot

## מה יש בתיקייה?

```
📁 diff-visualizer-bot/
├── 🤖 diff_bot.py          # קוד הבוט הראשי
├── 📋 requirements.txt      # תלויות Python
├── ⚙️ render.yaml          # קונפיגורציה לרנדר
├── 🐍 runtime.txt          # גרסת Python
├── 📝 README.md            # תיעוד מלא
├── 🚀 DEPLOY.md            # מדריך פריסה
├── 🧪 test_diff.py         # בדיקה מקומית
├── ▶️ start.sh             # סקריפט הרצה
├── 🔐 .env.example         # תבנית למשתני סביבה
├── 🚫 .gitignore          # קבצים להתעלם ב-git
└── 📄 LICENSE              # רישיון MIT

```

## 🎯 3 שלבים למען הבוט רץ

### 1️⃣ קבל טוכן בוט (דקה אחת)

```
1. פתח @BotFather בטלגרם
2. שלח: /newbot
3. תן שם: "My Diff Bot"
4. תן username: "my_diff_bot"
5. שמור את הטוקן!
```

### 2️⃣ העלה לגיטהאב (2 דקות)

```bash
# צור repository חדש ב-github.com
# ואז:

git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_NAME/diff-bot.git
git push -u origin main
```

### 3️⃣ פרוס ברנדר (3 דקות)

```
1. לך ל-render.com
2. New + → Blueprint
3. בחר את ה-repository
4. הוסף: TELEGRAM_BOT_TOKEN=YOUR_TOKEN
5. לחץ Apply
6. המתן... סיימת! ✅
```

## 💻 הרצה מקומית (לפיתוח)

```bash
# התקן תלויות
pip install -r requirements.txt

# צור .env
cp .env.example .env
# ערוך .env והכנס את הטוקן

# הרץ את הבוט
python diff_bot.py
```

או פשוט:
```bash
./start.sh
```

## 🧪 בדיקה מקומית (ללא טלגרם)

```bash
python test_diff.py
```

זה יוצר `test_diff.html` שאפשר לפתוח בדפדפן!

## 📖 איך להשתמש בבוט

1. פתח את הבוט בטלגרם
2. `/start` → "התחל השוואה חדשה"
3. שלח קוד 1
4. שלח קוד 2
5. קבל Diff! 🎉

### דוגמה:

**קוד 1:**
```python
def greet():
    print("Hello")
```

**קוד 2:**
```python
def greet(name):
    print(f"Hello {name}!")
```

**תוצאה:**
```
➖ def greet():
➕ def greet(name):
➖     print("Hello")
➕     print(f"Hello {name}!")
```

## 🎨 פיצ'רים

✅ השוואת קוד עם Diff צבעוני
✅ תמיכה בכל שפות התכנות
✅ קבצים או טקסט חופשי
✅ ייצוא ל-HTML
✅ סטטיסטיקות על שינויים
✅ ממשק בעברית

## 🔧 פתרון בעיות

**הבוט לא עונה?**
- בדוק שהטוקן נכון
- בדוק את ה-Logs ברנדר
- עשה Manual Deploy מחדש

**שגיאות בקוד?**
```bash
pip install -r requirements.txt --upgrade
```

**שאלות?**
- קרא את README.md המלא
- קרא את DEPLOY.md
- פתח Issue ב-GitHub

## 📚 תיעוד מלא

- **README.md** - תיעוד מקיף בעברית
- **DEPLOY.md** - מדריך פריסה מפורט
- **קוד הבוט** - מתועד היטב עם הסברים

## 🎓 למה לעשות עם זה?

- 🔍 להשוות גרסאות של קוד
- 📝 לראות מה השתנה בין commits
- 👥 לשתף שינויים עם הצוות
- 📱 לעשות code review בטלגרם
- 🎓 ללמוד Git diff בצורה ויזואלית

## 🚀 השלבים הבאים

1. **התאם אישית** - שנה צבעים, סגנון, הודעות
2. **הוסף פיצ'רים** - תמיכה בתמונות, PDFs
3. **שפר** - הוסף לוגיקת caching, webhooks
4. **שתף** - פתח PR עם שיפורים!

## ❤️ תודות

בוט זה נבנה עם:
- Python 3.11
- python-telegram-bot
- difflib (built-in)
- ואהבה לקוד נקי! 😊

---

**יש שאלות? צריך עזרה?**
פתח Issue או שלח PR! 🤝

**בהצלחה! 🎉**
