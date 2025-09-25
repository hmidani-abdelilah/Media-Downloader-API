import os
import uuid
import subprocess
import shutil
import re
from fastapi import FastAPI, Request, Form, BackgroundTasks, Query
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException
import yt_dlp
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],  # يسمح بالوصول من أي مصدر. قم بتقييد هذا في الإنتاج
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)


templates = Jinja2Templates(directory="templates")

DOWNLOADS_DIR = "downloads"
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

FFMPEG_CMD = 'ffmpeg -i "{input}" -vn -ab 128k -ar 44100 -y "{output}"'

def is_valid_url(url):
    pattern = r"^(https?://)[^\s]+$"
    return re.match(pattern, url.strip())

def is_valid_quality(quality):
    if quality is None:
        return False
    if quality == "mp3":
        return True
    pattern = r"^\d{3,4}p\s[a-zA-Z0-9]+$"
    return re.match(pattern, quality.strip())

def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "_", filename)

@app.get("/", response_class=HTMLResponse)
async def form_get(request: Request):
    return templates.TemplateResponse("form.html", {
        "request": request,
        "formats": None,
        "url": "",
        "is_playlist": False,
        "playlist_entries": None
    })

@app.post("/analyze", response_class=HTMLResponse)
async def analyze(request: Request, url: str = Form(...)):
    if not is_valid_url(url):
        return templates.TemplateResponse("form.html", {
            "request": request,
            "error": "الرابط غير صالح أو غير مدعوم.",
            "formats": None,
            "url": url,
            "is_playlist": False,
            "playlist_entries": None
        })
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)

        is_playlist = info.get('_type') == 'playlist'
        if is_playlist:
            titles = [entry.get("title") for entry in info.get("entries", [])]
            return templates.TemplateResponse("form.html", {
                "request": request,
                "formats": None,
                "url": url,
                "is_playlist": True,
                "playlist_title": info.get("title"),
                "playlist_entries": titles,
            })

        formats = info.get("formats", [])
        # عرض جميع الجودات مع الامتداد
        quality_options = sorted({f"{f['height']}p {f['ext']}" for f in formats if f.get('height') and f.get('ext')})
        quality_options.append("mp3")

        return templates.TemplateResponse("form.html", {
            "request": request,
            "formats": quality_options,
            "title": info.get("title"),
            "url": url,
            "is_playlist": False,
            "playlist_entries": None
        })

    except Exception as e:
        return templates.TemplateResponse("form.html", {
            "request": request,
            "error": f"حدث خطأ: {str(e)}",
            "formats": None,
            "url": url,
            "is_playlist": False,
            "playlist_entries": None
        })

def convert_to_mp3(input_path: str, output_path: str):
    cmd = FFMPEG_CMD.format(input=input_path, output=output_path)
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.exists(input_path):
        os.remove(input_path)

@app.post("/download", response_class=HTMLResponse)
async def download(
    request: Request,
    url: str = Form(...),
    quality: str = Form(None),  # غير إجباري للفيديوهات الفردية
    playlist_download_type: str = Form(None),
    background_tasks: BackgroundTasks = None
):
    if not is_valid_url(url):
        return templates.TemplateResponse("form.html", {
            "request": request,
            "error": "الرابط غير صالح أو غير مدعوم.",
            "formats": None,
            "url": url,
            "is_playlist": False,
            "playlist_entries": None
        })
    if not playlist_download_type and not is_valid_quality(quality):
        return templates.TemplateResponse("form.html", {
            "request": request,
            "error": "صيغة الجودة غير صحيحة أو غير مدعومة.",
            "formats": None,
            "url": url,
            "is_playlist": False,
            "playlist_entries": None
        })
    try:
        # تحميل قائمة تشغيل
        if playlist_download_type:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)

            if info.get('_type') != 'playlist':
                return templates.TemplateResponse("form.html", {
                    "request": request,
                    "error": "الرابط ليس قائمة تشغيل.",
                    "formats": None,
                    "url": url,
                    "is_playlist": False,
                    "playlist_entries": None
                })

            folder_name = info.get("title", "playlist").replace('/', '_').replace('\\', '_')
            folder_path = os.path.join(DOWNLOADS_DIR, folder_name)
            os.makedirs(folder_path, exist_ok=True)

            if playlist_download_type == "playlist_video":
                ydl_opts = {
                    'format': 'bestvideo+bestaudio/best',
                    'outtmpl': os.path.join(folder_path, '%(title)s.%(ext)s'),
                    'quiet': True,
                    'merge_output_format': 'mp4',
                    'external_downloader': 'aria2c',
                    'external_downloader_args': [
                        '--min-split-size=1M',
                        '--max-connection-per-server=16',
                        '--max-concurrent-downloads=16',
                        '--split=16'
                    ],
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

            elif playlist_download_type == "playlist_mp3":
                for entry in info.get("entries", []):
                    title = entry['title'].replace('/', '_').replace('\\', '_')
                    tmp_file = os.path.join(folder_path, f"{title}.webm")
                    mp3_file = os.path.join(folder_path, f"{title}.mp3")

                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': tmp_file,
                        'quiet': True,
                        'external_downloader': 'aria2c',
                        'external_downloader_args': [
                            '--min-split-size=1M',
                            '--max-connection-per-server=16',
                            '--max-concurrent-downloads=16',
                            '--split=16'
                        ],
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([entry['webpage_url']])

                    convert_to_mp3(tmp_file, mp3_file)

            else:
                return templates.TemplateResponse("form.html", {
                    "request": request,
                    "error": "خيار تحميل قائمة التشغيل غير معروف.",
                    "formats": None,
                    "url": url,
                    "is_playlist": True,
                    "playlist_entries": [e.get("title") for e in info.get("entries", [])]
                })

            # إنشاء ملف مضغوط للتحميل
            zip_path = shutil.make_archive(base_name=os.path.join(DOWNLOADS_DIR, folder_name), format='zip', root_dir=folder_path)
            
            # جدولة حذف مجلد التحميل بعد انتهاء المهمة
            shutil.rmtree(folder_path)
            if background_tasks:
                background_tasks.add_task(os.remove, zip_path)

            return FileResponse(zip_path, filename=f"{folder_name}.zip", media_type='application/zip')

        # تحميل فيديو أو صوت مفرد - يجب تحديد جودة
        if not quality:
            raise HTTPException(status_code=422, detail="حقل الجودة (quality) مطلوب لتحميل الفيديو الفردي")

        file_id = str(uuid.uuid4())
        # لاحظ: لا تحدد الامتداد هنا، سيتم تحديده لاحقاً حسب الجودة المختارة
        temp_path = os.path.join(DOWNLOADS_DIR, f"{file_id}")
        output_path = os.path.join(DOWNLOADS_DIR, f"{file_id}.mp3")

        if quality == "mp3":
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': temp_path,
                'quiet': True,
                'external_downloader': 'aria2c',
                'external_downloader_args': [
                    '--min-split-size=1M',
                    '--max-connection-per-server=16',
                    '--max-concurrent-downloads=16',
                    '--split=16'
                ],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            convert_to_mp3(temp_path, output_path)
            
            if background_tasks:
                background_tasks.add_task(os.remove, output_path)
            return FileResponse(output_path, filename="audio.mp3", media_type="audio/mpeg")

        else:
            # استخراج الجودة والامتداد
            try:
                parts = quality.strip().split()
                if len(parts) != 2:
                    raise ValueError()
                q_height, q_ext = parts
                q_height = int(q_height.replace('p', '').strip())
                q_ext = q_ext.strip()
            except Exception:
                return templates.TemplateResponse("form.html", {
                    "request": request,
                    "error": "صيغة الجودة غير صحيحة. مثال: 720p mp4",
                    "formats": None,
                    "url": url,
                    "is_playlist": False,
                    "playlist_entries": None
                })

            file_id = str(uuid.uuid4())
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
            video_title = sanitize_filename(info.get("title", "video"))  # استخدم الدالة هنا
            out_file = os.path.join(DOWNLOADS_DIR, f"{file_id}_{video_title}.{q_ext}")

            # استخدم صيغة دمج تلقائي للفيديو والصوت
            ydl_format = f"bestvideo[height={q_height}][ext={q_ext}]+bestaudio/best[ext=m4a]/best[height={q_height}][ext={q_ext}]"

            ydl_opts = {
                'format': ydl_format,
                'outtmpl': out_file,
                'quiet': True,
                'merge_output_format': q_ext,
                'external_downloader': 'aria2c',
                'external_downloader_args': [

                    '--min-split-size=1M',

                    '--max-connection-per-server=16',

                    '--max-concurrent-downloads=16',

                    '--split=16'],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            if background_tasks:
                background_tasks.add_task(os.remove, out_file)
            return FileResponse(out_file, filename=f"{video_title}.{q_ext}", media_type=f"video/{q_ext}")

    except Exception as e:
        return templates.TemplateResponse("form.html", {
            "request": request,
            "error": f"حدث خطأ أثناء التحميل: {str(e)}",
            "formats": None,
            "url": url,
            "is_playlist": False,
            "playlist_entries": None
        })
    
@app.get("/download")
async def download_get(
    url: str = Query(...),
    quality: str = Query(None),
    background_tasks: BackgroundTasks = None
):
    if not is_valid_url(url):
        raise HTTPException(status_code=422, detail="الرابط غير صالح أو غير مدعوم.")
    if not is_valid_quality(quality):
        raise HTTPException(status_code=422, detail="صيغة الجودة غير صحيحة أو غير مدعومة.")

    try:
        file_id = str(uuid.uuid4())
        temp_path = os.path.join(DOWNLOADS_DIR, f"{file_id}")
        output_path = os.path.join(DOWNLOADS_DIR, f"{file_id}.mp3")

        if quality == "mp3":
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': temp_path,
                'quiet': True,
                'external_downloader': 'aria2c',
                'external_downloader_args': [
                    '--min-split-size=1M',
                    '--max-connection-per-server=16',
                    '--max-concurrent-downloads=16',
                    '--split=16'
                ],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            convert_to_mp3(temp_path, output_path)
            
            if background_tasks:
                background_tasks.add_task(os.remove, output_path)
            return FileResponse(output_path, filename="audio.mp3", media_type="audio/mpeg")

        else:
            # استخراج الجودة والامتداد
            try:
                parts = quality.strip().split()
                if len(parts) != 2:
                    raise ValueError()
                q_height, q_ext = parts
                q_height = int(q_height.replace('p', '').strip())
                q_ext = q_ext.strip()
            except Exception:
                raise HTTPException(status_code=422, detail="صيغة الجودة غير صحيحة. مثال: 720p mp4")

            file_id = str(uuid.uuid4())
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
            video_title = sanitize_filename(info.get("title", "video"))  # استخدم الدالة هنا
            out_file = os.path.join(DOWNLOADS_DIR, f"{file_id}_{video_title}.{q_ext}")

            # استخدم صيغة دمج تلقائي للفيديو والصوت
            ydl_format = f"bestvideo[height={q_height}][ext={q_ext}]+bestaudio/best[ext=m4a]/best[height={q_height}][ext={q_ext}]"

            ydl_opts = {
                'format': ydl_format,
                'outtmpl': out_file,
                'quiet': True,
                'merge_output_format': q_ext,
                'external_downloader': 'aria2c',
                'external_downloader_args': [
                    '--min-split-size=1M',
                    '--max-connection-per-server=16',
                    '--max-concurrent-downloads=16',
                    '--split=16'
                ],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            if background_tasks:
                background_tasks.add_task(os.remove, out_file)
            return FileResponse(out_file, filename=f"{video_title}.{q_ext}", media_type=f"video/{q_ext}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"حدث خطأ أثناء التحميل: {str(e)}")
