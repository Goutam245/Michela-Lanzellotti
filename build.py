# -*- coding: utf-8 -*-
"""Assembla le pagine statiche in public/ a partire da src/ e dai motivi in svg/.

Uso:  python gen_svg.py && python prep_images.py && python build.py
"""
import os, re, shutil, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
SVG = os.path.join(ROOT, "svg")
OUT = os.path.join(ROOT, "public")

WA_NUM = "390000000000"          # il numero di prova del brief: +39 000 000 0000
WA_TEXT = "Ciao%20Michela%2C%20ho%20visto%20il%20sito%20e%20vorrei%20parlarti%20del%20mio%20abito."

TOKENS = {
    "WA": f"https://wa.me/{WA_NUM}?text={WA_TEXT}",
    "WA_NUM": WA_NUM,
    "IG": "#",
    "MAIL": "test@example.com",
}


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def resolve(text, depth=0):
    """Sostituisce {{nome}} con: un file svg/, un parziale src/_nome.html, o un token."""
    if depth > 8:
        raise RuntimeError("inclusioni troppo annidate")

    def sub(m):
        key = m.group(1).strip()
        if key in TOKENS:
            return TOKENS[key]
        svg_path = os.path.join(SVG, key.lower() + ".svg")
        if os.path.exists(svg_path):
            return read(svg_path)
        part = os.path.join(SRC, "_" + key.lower() + ".html")
        if os.path.exists(part):
            return resolve(read(part), depth + 1)
        raise RuntimeError(f"segnaposto non risolto: {{{{{key}}}}}")

    return re.sub(r"\{\{([A-Za-z0-9_]+)\}\}", sub, text)


def avvolgi_webp(html):
    """Avvolge ogni <img> jpg in un <picture> con la variante webp davanti.

    Il markup nei sorgenti resta leggibile: la doppia sorgente la mette il build.
    """
    def sostituisci(m):
        tag = m.group(0)
        if ".jpg" not in tag:
            return tag
        srcset = re.search(r'\ssrcset="([^"]+)"', tag)
        sizes = re.search(r'\ssizes="([^"]+)"', tag)
        src = re.search(r'\ssrc="([^"]+)"', tag)
        elenco = srcset.group(1) if srcset else (src.group(1) if src else "")
        if not elenco:
            return tag
        webp = elenco.replace(".jpg", ".webp")
        attr_sizes = f' sizes="{sizes.group(1)}"' if sizes else ""
        return f'<picture><source type="image/webp" srcset="{webp}"{attr_sizes}>{tag}</picture>'

    html = re.sub(r"<img\b[^>]*>", sostituisci, html)
    # anche il precaricamento dell'immagine di apertura punta al webp
    html = html.replace(
        '<link rel="preload" as="image" href="assets/img/abito-pizzo-fronte-800.jpg" '
        'imagesrcset="assets/img/abito-pizzo-fronte-800.jpg 800w, assets/img/abito-pizzo-fronte.jpg 1200w"',
        '<link rel="preload" as="image" type="image/webp" href="assets/img/abito-pizzo-fronte-800.webp" '
        'imagesrcset="assets/img/abito-pizzo-fronte-800.webp 800w, assets/img/abito-pizzo-fronte.webp 1200w"',
    )
    return html


def main():
    os.makedirs(OUT, exist_ok=True)
    pages = [f for f in os.listdir(SRC) if f.endswith(".html") and not f.startswith("_")]
    for page in sorted(pages):
        html = avvolgi_webp(resolve(read(os.path.join(SRC, page))))
        left = re.findall(r"\{\{[^}]+\}\}", html)
        if left:
            print(f"  ! segnaposto rimasti in {page}: {left}", file=sys.stderr)
        dest = os.path.join(OUT, page)
        with open(dest, "w", encoding="utf-8", newline="\n") as f:
            f.write(html)
        print(f"  {page:24s} {len(html)/1024:7.1f} KB")

    # file statici copiati così come sono
    for name in ("robots.txt", "_headers", "_redirects"):
        s = os.path.join(SRC, name)
        if os.path.exists(s):
            shutil.copy(s, os.path.join(OUT, name))
            print(f"  {name}")


if __name__ == "__main__":
    print("costruzione in public/")
    main()
    print("fatto.")
