# -*- coding: utf-8 -*-
"""Prepara le immagini del sito: ritagli, ridimensionamenti, varianti logo, favicon."""
from PIL import Image, ImageOps
import numpy as np, os, shutil

SRC = r"C:\Users\Goutam\Downloads\03 Michela Lanzellotti-20260830T172823Z-1-001\03 Michela Lanzellotti"
FOTO = os.path.join(SRC, "foto")
LOGO = os.path.join(SRC, "logo")
OUT_IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public", "assets", "img")
OUT_LOGO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public", "assets", "logo")
os.makedirs(OUT_IMG, exist_ok=True); os.makedirs(OUT_LOGO, exist_ok=True)

def save(im, name, width, quality=84, out=OUT_IMG):
    im = im.convert("RGB")
    if im.width > width:
        h = round(im.height * width / im.width)
        im = im.resize((width, h), Image.LANCZOS)
    p = os.path.join(out, name)
    im.save(p, "JPEG", quality=quality, optimize=True, progressive=True, subsampling=1)
    # variante webp: stessa immagine, circa metà del peso
    pw = os.path.splitext(p)[0] + ".webp"
    im.save(pw, "WEBP", quality=max(72, quality - 6), method=6)
    print(f"  {name:34s} {im.size}  jpg {os.path.getsize(p)/1024:6.1f} KB"
          f"  webp {os.path.getsize(pw)/1024:6.1f} KB")

def variants(src_path, stem, widths, crop=None, quality=84):
    im = Image.open(src_path)
    im = ImageOps.exif_transpose(im)
    if crop: im = im.crop(crop)
    print(f"{stem}  <- {os.path.basename(src_path)}  {im.size}")
    for w in widths:
        suffix = "" if w == widths[0] else f"-{w}"
        save(im, f"{stem}{suffix}.jpg", w, quality)

# ---------------------------------------------------------------- suoi abiti
variants(os.path.join(FOTO,"SaveClip.App_762974370_18359131576301191_5773374508985029644_n.jpg"),
         "abito-pizzo-fronte", [1200, 800])
variants(os.path.join(FOTO,"SaveClip.App_767131059_18359131630301191_7987123687398040777_n.jpg"),
         "abito-pizzo-schiena", [900, 700])
variants(os.path.join(FOTO,"SaveClip.App_768408902_18359277616301191_6568143450857410105_n.jpg"),
         "abito-corto-terrazza", [1500, 1000, 700], quality=82)
variants(os.path.join(FOTO,"SaveClip.App_769007271_18359131567301191_5705365447028832648_n.jpg"),
         "abito-specchio", [900, 700])
variants(os.path.join(FOTO,"SaveClip.App_769032754_18359131621301191_7585544025041180032_n.jpg"),
         "abito-consolle", [1200, 800])
# comunione: rimosse le bande nere sopra e sotto (righe 143-995)
variants(os.path.join(FOTO,"SaveClip.App_689060932_1267699301763054_6059286054342292240_n.jpg"),
         "abito-comunione", [640], crop=(0,143,640,996), quality=88)

# ---------------------------------------------------------------- atmosfera Puglia
variants(os.path.join(FOTO,"01901665-2461-401c-bf25-1c9fec4aa290.jpg"),
         "puglia-trullo", [1200, 800])
variants(os.path.join(FOTO,"Trulli restoration_.jpeg"),
         "puglia-trulli-sera", [735])

# ---------------------------------------------------------------- ritratto (barra nera rimossa)
variants(os.path.join(FOTO,"11.jpg"), "michela-ritratto", [718], crop=(0,0,718,962), quality=88)

# ---------------------------------------------------------------- logo
src_logo = Image.open(os.path.join(LOGO,"logo-ml-nero.png")).convert("RGBA")
bbox = src_logo.getbbox()
print("logo bbox:", bbox, "size", src_logo.size)
shutil.copy(os.path.join(LOGO,"logo-ml-nero.png"), os.path.join(OUT_LOGO,"logo-ml.png"))
print("  logo-ml.png (originale, invariato)")

# variante chiara: stesso identico tracciato, solo colorato di avorio per fondi scuri
alpha = src_logo.split()[3]
light = Image.new("RGBA", src_logo.size, (247, 242, 233, 0))
light.putalpha(alpha)
light.save(os.path.join(OUT_LOGO,"logo-ml-chiaro.png"))
print("  logo-ml-chiaro.png (stesso tracciato, tinta avorio)")

# ---------------------------------------------------------------- favicon
mark = src_logo.crop(bbox)
BG = (247, 240, 230, 255)
def favicon(size, name, pad_ratio=0.13, bg=BG):
    canvas = Image.new("RGBA", (size, size), bg)
    inner = round(size * (1 - 2*pad_ratio))
    m = mark.copy()
    r = min(inner / m.width, inner / m.height)
    m = m.resize((max(1,round(m.width*r)), max(1,round(m.height*r))), Image.LANCZOS)
    canvas.alpha_composite(m, ((size - m.width)//2, (size - m.height)//2))
    canvas.save(os.path.join(OUT_LOGO, name))
    print(f"  {name} {size}x{size}")
    return canvas
favicon(16, "favicon-16.png", 0.06)
favicon(32, "favicon-32.png", 0.08)
favicon(180, "apple-touch-icon.png", 0.14)
favicon(192, "icon-192.png", 0.14)
favicon(512, "icon-512.png", 0.14)
ico = favicon(64, "_tmp.png", 0.08)
ico.convert("RGB").save(os.path.join(OUT_LOGO, "favicon.ico"), sizes=[(16,16),(32,32),(48,48)])
os.remove(os.path.join(OUT_LOGO,"_tmp.png"))
print("  favicon.ico")
