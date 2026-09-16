import json, os, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
UA={"User-Agent":"dobutsu-shogi-design/0.1"}
OUT = os.path.join(ROOT, 'docs/design/wood')
os.makedirs(OUT,exist_ok=True)
SLUGS={"fine":"fine_grained_wood","maple":"white_maple_veneer","ash":"ash_veneer",
       "sycamore":"japanese_sycamore","cherry":"cherry_veneer","oak":"oak_veneer_01"}
def get(u):
    with urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=90) as r: return r.read()
for key,slug in SLUGS.items():
    try:
        d=json.loads(get(f"https://api.polyhaven.com/files/{slug}").decode())
        url=d["Diffuse"]["1k"]["jpg"]["url"]
        raw=f"{key}_1k.jpg"; open(raw,"wb").write(get(url))
        im=Image.open(raw).convert("RGB")
        w,h=im.size
        # 코마 한 장 크기의 영역만 잘라 쓴다 - 1K 전체를 축소하면 결이 뭉개진다
        s=min(w,h)//2
        im=im.crop((w//2-s//2,h//2-s//2,w//2+s//2,h//2+s//2)).resize((420,420),Image.LANCZOS)
        im.save(os.path.join(OUT,f"{key}.jpg"),quality=76,optimize=True)
        print("OK",key,slug,os.path.getsize(os.path.join(OUT,f"{key}.jpg"))//1024,"KB")
    except Exception as e:
        print("FAIL",key,e)
