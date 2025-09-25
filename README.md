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
* 🗜️​ يدعم تحميل القوائم ويستخرجها كملف zip 
*⚡ تحويل صوتي باستخدام `ffmpeg`.
* أداة `Aria2` الشهيرة لتجزئة التحميل وتسريعه.
*  🧽 حذف الملفات المؤقتة تلقائيًا بعد انتهاء التحميل.
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

* Ubuntu/Debian:
- تثبيت Aria2
```bash
sudo apt install aria2
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
## طريقة استخدام docker 
-  الحاوية مبنية باستخدام Ubuntu وتحتوي على جميع التبعيات اللازمة لتشغيل التطبيق بسهولة.
* 🐳 بناء وتشغيل الحاوية باستخدام Docker
1. نسخ المشروع
```bash
git clone https://github.com/hmidani-abdelilah/Media-Downloader-API.git
cd Media-Downloader-API
```
2. بناء صورة Docker
```bash
docker build -t media-downloader-api .
```
3. تشغيل الحاوية
```bash
docker run -p 8090:8000 --name media-downloader media-downloader-api
```
* سيعمل التطبيق على `http://localhost:8090`

## 🔍 الواجهة التفاعلية (Swagger UI)
بعد تشغيل الحاوية، يمكنك استعراض الواجهة التفاعلية عبر المتصفح:

```bash
http://localhost:8090/docs
```

## 🧱 مكونات Dockerfile
* ✅ نظام التشغيل الأساسي: Ubuntu

* ✅ تثبيت التبعيات: Python 3، FFmpeg، Git

* ✅ تحميل الكود: يتم استنساخه من GitHub مباشرة

* ✅ بيئة افتراضية: باستخدام venv

* ✅ تشغيل FastAPI: عبر uvicorn على المنفذ 8000

## 🔧 منفذ API
8000: المنفذ الداخلي للتطبيق داخل الحاوية

8090: المنفذ الخارجي على جهازك المحلي (عند تشغيل الحاوية بالأمر أعلاه)

📦 مثال على استخدام curl
```bash
curl -X POST "http://localhost:8090/download" -H  "accept: application/json" -H  "Content-Type: application/json" -d '{"url": "https://example.com/video"}'
```
غيّر "https://example.com/video" بالرابط الفعلي الذي تريد تحميله.


# او استخدم docker-compser
📦 خطوات الاستخدام:
1. تشغيل باستخدام Docker Compose
2. شغّل الخدمة:
```bash
docker-compose up --build
```
3. لإيقاف الحاوية:
```bash
docker-compose down
```
## الحاوية في docker Hub مباشرة من دون البناء 
[https://hub.docker.com/r/abdelilahxq/media-downloader-api](https://hub.docker.com/r/abdelilahxq/media-downloader-api)

## 📦 الحزم المستخدمة

* [`FastAPI`](https://fastapi.tiangolo.com/) — لبناء واجهة برمجة التطبيقات.
* [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) — لتحميل الفيديوهات من مصادر متعددة.
* [`Jinja2`](https://jinja.palletsprojects.com/) — لعرض صفحات HTML ديناميكية.
* [`Uvicorn`](https://www.uvicorn.org/) — لتشغيل FastAPI.
* [`python-multipart`](https://andrew-d.github.io/python-multipart/) — لدعم رفع الملفات والنماذج.
* [`pydub`](https://github.com/jiaaro/pydub) — اختياري لتحسين التعامل مع الصوتيات.

---

