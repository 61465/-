import os
import requests
from PIL import Image
import io
import zipfile  # مكتبة لضغط الملفات

class AICharacterScout:
    def __init__(self, api_key, cx, download_path="game_assets"):
        self.api_key = api_key
        self.cx = cx
        self.download_path = download_path
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)

    def is_safe(self, data):
        try:
            img = Image.open(io.BytesIO(data))
            img.verify()
            img = Image.open(io.BytesIO(data))
            img.load()
            if img.format not in ['PNG', 'JPEG', 'JPG', 'WEBP']:
                return False, None
            return True, img.format.lower()
        except:
            return False, None

    def search_and_download(self, char_name):
        print(f"🔍 فحص وتأمين: {char_name}...")
        search_url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'q': f"{char_name} game character full body render png",
            'cx': self.cx, 'key': self.api_key, 'searchType': 'image', 'num': 1
        }
        try:
            res = requests.get(search_url, params=params)
            items = res.json().get('items')
            if not items: return
            
            img_url = items[0]['link']
            img_res = requests.get(img_url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            safe, ext = self.is_safe(img_res.content)
            
            if safe:
                clean_name = char_name.replace(" ", "_").lower()
                path = os.path.join(self.download_path, f"{clean_name}.{ext}")
                with open(path, "wb") as f:
                    f.write(img_res.content)
                print(f"✅ تم حفظ: {clean_name}")
        except: pass

    def create_zip_archive(self):
        """وظيفة لجمع كل الصور في ملف ZIP واحد"""
        zip_name = "all_characters.zip"
        print(f"\n📦 جاري إنشاء ملف المضغوط: {zip_name}...")
        with zipfile.ZipFile(zip_name, 'w') as zipf:
            for root, dirs, files in os.walk(self.download_path):
                for file in files:
                    zipf.write(os.path.join(root, file), file)
        print(f"✨ اكتمل! الملف جاهز الآن للتحميل: {os.path.abspath(zip_name)}")

# --- الإعدادات ---
MY_API_KEY = "AIzaSyDnqyfWbDP_5oe05Kkggi13ovNfR-8bNHE"
MY_CX = "e1647720042a846ec"

scout = AICharacterScout(MY_API_KEY, MY_CX)

# القائمة (اختصار للتجربة)
character_names = ["Geralt of Rivia", "Arthur Morgan", "Master Chief", "Ezio Auditore", "Joel Miller"]

for name in character_names:
    scout.search_and_download(name)

# ضغط الملفات بعد الانتهاء
scout.create_zip_archive()
