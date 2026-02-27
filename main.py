import os
import requests
from PIL import Image
import io

class AICharacterScout:
    def __init__(self, api_key, cx, download_path="secure_assets"):
        self.api_key = api_key
        self.cx = cx
        self.download_path = download_path
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)

    def is_safe(self, data):
        """نظام فحص أمان الصور لمنع الملفات المفخخة"""
        try:
            img = Image.open(io.BytesIO(data))
            img.verify()  # فحص هيكلية الملف
            img = Image.open(io.BytesIO(data))
            img.load()    # معالجة البكسلات للتأكد من خلوها من ثغرات الذاكرة
            
            # السماح بالصيغ الآمنة فقط
            if img.format not in ['PNG', 'JPEG', 'JPG', 'WEBP']:
                return False, None
            return True, img.format.lower()
        except:
            return False, None

    def search_and_download(self, char_name):
        print(f"🔍 جاري البحث وتأمين صورة: {char_name}...")
        search_url = "https://www.googleapis.com/customsearch/v1"
        
        # كلمات بحث دقيقة للحصول على صور مفرغة عالية الجودة (Renders)
        query = f"{char_name} game character full body render png"
        
        params = {
            'q': query,
            'cx': self.cx,
            'key': self.api_key,
            'searchType': 'image',
            'num': 1
        }

        try:
            res = requests.get(search_url, params=params)
            results = res.json().get('items')
            
            if not results:
                print(f"❓ لم يتم العثور على نتائج لـ {char_name}")
                return

            img_url = results[0]['link']
            img_res = requests.get(img_url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
            
            # مرحلة الفحص الأمني قبل الحفظ
            safe, ext = self.is_safe(img_res.content)

            if safe:
                clean_name = char_name.replace(" ", "_").lower()
                path = os.path.join(self.download_path, f"{clean_name}.{ext}")
                with open(path, "wb") as f:
                    f.write(img_res.content)
                print(f"✅ تم الفحص والتحميل: {clean_name}.{ext}")
            else:
                print(f"🛡️ حظر أمني: تم استبعاد صورة {char_name} لأنها مريبة.")
                
        except Exception as e:
            print(f"⚠️ خطأ مع {char_name}: {e}")

# --- الإعدادات والمفاتيح ---
MY_API_KEY = "ضغAIzaSyDnqyfWbDP_5oe05Kkggi13ovNfR-8bNHE" 
MY_CX = "e1647720042a846ec" # المعرف الخاص بك من الصورة

scout = AICharacterScout(MY_API_KEY, MY_CX)

# --- قائمة الـ 100 شخصية الكاملة ---
character_names = [
    # 1. AI
    "GLaDOS Portal", "HK-47 Star Wars", "SHODAN System Shock", "Cortana Halo", "EDI Mass Effect",
    "Durandal Marathon", "Amon SOMA", "Claptrap Borderlands", "Wheatley Portal 2", "Legion Mass Effect",
    # 2. Soldiers
    "Master Chief", "Captain Price MW", "Soap MacTavish", "Simon Ghost Riley", "Marcus Fenix Gears",
    "Sam Gideon Vanquish", "Nomad Ghost Recon", "Vasily Zaitsev CoD", "Sgt Johnson Halo", "Nick Reyes CoD",
    # 3. Witchers
    "Geralt of Rivia", "Vesemir Witcher", "Eskel Witcher", "Lambert Witcher", "Letho of Gulet",
    "Ciri Witcher 3", "Triss Merigold", "Yennefer of Vengerberg", "Emiel Regis Witcher", "Dandelion Witcher",
    # 4. Assassins
    "Ezio Auditore", "Altair Ibn-LaAhad", "Connor Kenway", "Edward Kenway", "Arno Dorian",
    "Jacob Frye", "Evie Frye", "Bayek of Siwa", "Kassandra Assassins Creed", "Alexios Assassins Creed",
    # 5. Outlaws
    "Arthur Morgan RDR2", "John Marston RDR1", "Dutch van der Linde", "Sadie Adler", "Bill Williamson",
    "Javier Escuella", "Charles Smith RDR2", "Micah Bell", "Landon Ricketts", "Red Harlow",
    # 6. Survivors
    "Ellie Williams TLOU", "Joel Miller TLOU", "Tommy Miller TLOU", "Abby Anderson", "Lev TLOU2",
    "Yara TLOU2", "Bill TLOU1", "Tess TLOU1", "Marlene TLOU1", "Dina TLOU2",
    # 7. Heroes
    "Link Zelda TotK", "Princess Zelda", "Ganondorf TotK", "Mario Nintendo", "Luigi Nintendo",
    "Princess Peach", "Yoshi Nintendo", "Kirby", "Samus Aran Metroid", "Fox McCloud",
    # 8. Hunters
    "Dante Devil May Cry", "Vergil DMC", "Nero DMC", "Trish DMC", "Lady DMC",
    "V Devil May Cry", "Doom Slayer", "Simon Belmont", "Alucard Castlevania", "Richter Belmont",
    # 9. Raiders
    "Lara Croft Shadow", "Nathan Drake", "Elena Fisher", "Victor Sullivan Uncharted", "Chloe Frazer",
    "Sam Drake Uncharted", "Aloy Horizon", "Rost Horizon", "Erend Horizon", "Sylens Horizon",
    # 10. Stealth
    "Solid Snake MGS2", "Big Boss MGS3", "Raiden Metal Gear", "Gray Fox MGS", "Sam Fisher Splinter Cell",
    "Adam Jensen Deus Ex", "Corvo Attano", "Emily Kaldwin", "Garrett Thief", "Agent 47 Hitman"
]

print(f"🔥 سيتم الآن معالجة {len(character_names)} شخصية بنظام الأمان الذكي...")

for name in character_names:
    scout.search_and_download(name)

print("\n✨ المهمة انتهت! تفقد مجلد secure_assets")