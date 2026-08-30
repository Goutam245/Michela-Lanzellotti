# -*- coding: utf-8 -*-
"""Controlli statici sulle pagine costruite: struttura, accessibilità, coerenza."""
import os, re, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(ROOT, "public")
problemi = []


def p(pagina, msg):
    problemi.append(f"{pagina}: {msg}")


for percorso in sorted(glob.glob(os.path.join(PUB, "*.html"))):
    nome = os.path.basename(percorso)
    s = open(percorso, encoding="utf-8").read()

    # lingua e titolo
    if 'lang="it"' not in s:
        p(nome, "manca lang=\"it\"")
    titolo = re.search(r"<title>(.*?)</title>", s, re.S)
    if not titolo:
        p(nome, "manca <title>")

    # indicizzazione
    if "noindex" not in s:
        p(nome, "manca il meta robots noindex")

    # un solo h1
    h1 = re.findall(r"<h1\b", s)
    if len(h1) != 1:
        p(nome, f"h1 presenti: {len(h1)} (dovrebbe essere 1)")

    # ordine dei livelli di titolo
    livelli = [int(m) for m in re.findall(r"<h([1-6])\b", s)]
    for a, b in zip(livelli, livelli[1:]):
        if b > a + 1:
            p(nome, f"salto di livello: h{a} -> h{b}")
            break

    # immagini con alt
    for m in re.finditer(r"<img\b[^>]*>", s):
        tag = m.group(0)
        if "alt=" not in tag:
            p(nome, f"img senza alt: {tag[:90]}")
        elif re.search(r'alt=""', tag) and 'id="lb-img"' not in tag:
            p(nome, f"alt vuoto: {tag[:90]}")
        if "width=" not in tag or "height=" not in tag:
            if 'id="lb-img"' not in tag:
                p(nome, f"img senza width/height: {tag[:90]}")

    # collegamenti
    for m in re.finditer(r"<a\b[^>]*>", s):
        tag = m.group(0)
        if "href=" not in tag:
            p(nome, f"a senza href: {tag[:80]}")
        if 'target="_blank"' in tag and "noopener" not in tag:
            p(nome, f"target=_blank senza rel=noopener: {tag[:80]}")

    # bottoni con tipo esplicito
    for m in re.finditer(r"<button\b[^>]*>", s):
        if "type=" not in m.group(0):
            p(nome, f"button senza type: {m.group(0)[:70]}")

    # riferimenti a file locali esistenti
    for m in re.finditer(r'(?:src|href)="((?:assets|)[^":#][^"]*)"', s):
        rif = m.group(1)
        if rif.startswith(("http", "mailto:", "#", "data:")):
            continue
        atteso = os.path.join(PUB, rif.split("?")[0].split("#")[0])
        if not os.path.exists(atteso):
            p(nome, f"riferimento inesistente: {rif}")

    # divieti del brief
    for parola in ("€", "prezzo di", "listino", "carrello", "aggiungi al", "acquista"):
        if parola.lower() in s.lower():
            p(nome, f"parola vietata trovata: {parola}")
    if re.search(r"\bvia [A-Z]", s) or "maps.google" in s or "google.com/maps" in s:
        p(nome, "possibile indirizzo o mappa")

print("PAGINE CONTROLLATE:", ", ".join(os.path.basename(x) for x in sorted(glob.glob(os.path.join(PUB, "*.html")))))
if problemi:
    print(f"\n{len(problemi)} PROBLEMI:")
    for x in problemi:
        print("  •", x)
else:
    print("\nnessun problema rilevato")
