# Media-Downloader-API
# 📥 أداة تحميل متعددة المنصات باستخدام FastAPI

تطبيق ويب مبني على FastAPI يتيح لك تحميل الفيديوهات أو قوائم التشغيل من عدة منصات مثل YouTube وFacebook وTikTok وX (Twitter سابقًا) وغيرها. يمكنك تحويل الفيديو إلى MP3 أو تحميله كفيديو بجودة محددة. يتميز التطبيق بواجهة استخدام بسيطة وسلسة باللغة العربية.

---

## ✅ المميزات

* 🔗 يدعم روابط الفيديو من منصات متعددة:

  * YouTube
  * Facebook
  * TikTok
  * X (Twitter)
  * وأكثر من ذلك (بفضل yt-dlp)
* 🎵 تحميل كـ MP3 أو كفيديو (mp4، webm...) بجودة محددة مثل "720p mp4".
* ⚡ تحويل صوتي باستخدام `ffmpeg`.
* 🧽 حذف الملفات المؤقتة تلقائيًا بعد انتهاء التحميل.
* 🌐 واجهة أمامية باللغة العربية تعتمد على HTML + Jinja2.

---

## 🧰 المتطلبات

* Python 3.8 أو أحدث
* أداة `ffmpeg` مثبتة في النظام (مطلوبة لتحويل الصوت إلى mp3)

### 🧪 خطوات الإعداد والتنصيب

1. **استنساخ المشروع:**

```bash
git clone https://github.com/hmidani-abdelilah/Media-Downloader-API.git
cd Media-Downloader-API
```

2. **إنشاء بيئة افتراضية (اختياري لكن موصى به):**

```bash
python -m venv Media-Downloader-API
source Media-Downloader-API/bin/activate  # على لينُكس أو ماك
Media-Downloader-API\Scripts\activate     # على ويندوز
```

3. **تنصيب التبعيات:**

```bash
pip install -r requirements.txt
```

4. **تأكد من أن ffmpeg مثبت ومتوفر:**

```bash
ffmpeg -version
```

إذا لم يكن مثبتًا، يمكنك تثبيته عبر:

* Ubuntu/Debian:

```bash
sudo apt install ffmpeg
```

* Windows: من [ffmpeg.org](https://ffmpeg.org/download.html)
* macOS:

```bash
brew install ffmpeg
```

---

## 🚀 تشغيل التطبيق

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

ثم افتح متصفحك على:

```
http://localhost:8001
```

---

## 📁 إعداد المجلدات

تأكد من وجود مجلد `downloads` لتخزين الملفات المؤقتة والنهائية:

```bash
mkdir -p downloads
```

---

## 📂 هيكل المشروع

```
.
├── main.py                      # التطبيق الرئيسي (FastAPI backend)
├── requirements.txt             # قائمة التبعيات
├── templates/                   # مجلد القوالب Jinja2
│   ├── form.html                # واجهة المستخدم
│   └── download_complete.html  # صفحة التأكيد بعد التحميل
├── downloads/                   # مجلد لتخزين الملفات المحملة
└── README.md                    # ملف التوثيق
```

---

## 🧪 طريقة الاستخدام

1. افتح المتصفح وادخل على `http://localhost:8001`
2. الصق رابط فيديو أو قائمة تشغيل من منصة مدعومة (YouTube, Facebook, TikTok...)
3. حدد الجودة أو اختر "MP3".
4. اضغط على زر "تحميل" للحصول على رابط مباشر للملف.

---

## 📦 الحزم المستخدمة

* [`FastAPI`](https://fastapi.tiangolo.com/) — لبناء واجهة برمجة التطبيقات.
* [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) — لتحميل الفيديوهات من مصادر متعددة.
* [`Jinja2`](https://jinja.palletsprojects.com/) — لعرض صفحات HTML ديناميكية.
* [`Uvicorn`](https://www.uvicorn.org/) — لتشغيل FastAPI.
* [`python-multipart`](https://andrew-d.github.io/python-multipart/) — لدعم رفع الملفات والنماذج.
* [`pydub`](https://github.com/jiaaro/pydub) — اختياري لتحسين التعامل مع الصوتيات.

---

