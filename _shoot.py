# -*- coding: utf-8 -*-
"""Strumento di sviluppo: fotografa le pagine di sezione con Chrome headless."""
import os, subprocess, sys, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(ROOT, "_shots")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
BASE = "http://127.0.0.1:4173/public"
os.makedirs(SHOTS, exist_ok=True)

larghezza = int(sys.argv[1]) if len(sys.argv) > 1 else 1440
altezza = int(sys.argv[2]) if len(sys.argv) > 2 else 1500
filtro = sys.argv[3] if len(sys.argv) > 3 else ""
etichetta = "m" if larghezza < 700 else "d"

pagine = sorted(os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "public", "_sez", "*.html")))
if filtro:
    pagine = [p for p in pagine if filtro in p]

for pagina in pagine:
    fuori = os.path.join(SHOTS, f"{etichetta}{larghezza}-{pagina.replace('.html', '')}.png")
    subprocess.run([
        CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
        "--force-device-scale-factor=1", "--virtual-time-budget=6000",
        f"--window-size={larghezza},{altezza}",
        f"--screenshot={fuori}",
        f"{BASE}/_sez/{pagina}",
    ], capture_output=True)
    print(f"  {os.path.basename(fuori):40s} {os.path.getsize(fuori)/1024:7.0f} KB" if os.path.exists(fuori) else f"  ! {pagina}")
