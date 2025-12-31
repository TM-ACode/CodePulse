# رفع المشروع على GitHub - خطوات سريعة

## الطريقة الأسهل (GitHub Desktop)

### 1. حمّل البرنامج
https://desktop.github.com

### 2. سجّل دخول
بحسابك في GitHub

### 3. أنشئ Repository جديد
- File → New Repository
- الاسم: `CodePulse`
- الوصف: `AI-powered code analysis tool`
- اضغط Create

### 4. انسخ الملفات
- افتح مجلد الـ Repository اللي أنشأته
- انسخ كل ملفات CodePulse للمجلد
- GitHub Desktop بيكتشف التغييرات تلقائياً

### 5. ارفع!
- اكتب رسالة: "Initial commit - CodePulse v0.2.0"
- اضغط Commit to main
- اضغط Publish repository
- خلّه Public (عشان الناس يشوفونه)
- اضغط Publish

**خلاص! مشروعك على GitHub! 🎉**

---

## الطريقة الثانية (الأوامر)

### 1. أنشئ Repository على الموقع
https://github.com/new
- الاسم: `CodePulse`
- Public
- بدون README (عندنا واحد)
- Create repository

### 2. افتح Terminal
```bash
cd /path/to/CodePulse

git init
git add .
git commit -m "Initial commit - CodePulse v0.2.0"

# غيّر YOUR-USERNAME باسمك
git remote add origin https://github.com/YOUR-USERNAME/CodePulse.git

git branch -M main
git push -u origin main
```

**انتهى! 🎉**

---

## بعد الرفع

### أضف Topics
في صفحة الـ Repository:
- Settings → About
- Topics: `python`, `code-analysis`, `security-scanner`, `ai`

### شارك المشروع
- LinkedIn
- Twitter
- Portfolio

---

## رابط مشروعك
```
github.com/YOUR-USERNAME/CodePulse
```

**للتفاصيل الكاملة، شوف: `GITHUB_UPLOAD_GUIDE.md`**

---

**بالتوفيق! 🚀**
