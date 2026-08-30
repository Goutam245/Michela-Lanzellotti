# -*- coding: utf-8 -*-
"""Verifica che ogni riga di COPY-IT.md compaia, identica, nel sito costruito."""
import html as H
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
COPY = r"C:\Users\Goutam\Downloads\03 Michela Lanzellotti-20260830T172823Z-1-001\03 Michela Lanzellotti\COPY-IT.md"
PAGINE = ["public/index.html", "public/informativa.html", "public/404.html"]


def testo_visibile(percorso):
    s = open(percorso, encoding="utf-8").read()
    s = re.sub(r"<svg\b.*?</svg>", " ", s, flags=re.S)
    s = re.sub(r"<script\b.*?</script>", " ", s, flags=re.S)
    s = re.sub(r"<style\b.*?</style>", " ", s, flags=re.S)
    s = re.sub(r"<head\b.*?</head>", " ", s, flags=re.S)
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    # i tag in linea non separano le parole, quelli di blocco sì
    s = re.sub(r"</?(?:a|em|strong|span|b|i|abbr)\b[^>]*>", "", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = H.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


sito = " ||| ".join(testo_visibile(os.path.join(ROOT, p)) for p in PAGINE)
sito_norm = re.sub(r"\s+", " ", sito)
# i segnaposto delle date del calendario non contano come testo
sito_norm = re.sub(r"\s*[—–]\s*", " ", sito_norm)

righe = [r.strip() for r in open(COPY, encoding="utf-8").read().split("\n")]
# le prime righe del file sono istruzioni per il grafico, non copy di pagina
inizio = righe.index("Michela Lanzellotti")
righe = righe[inizio:]

mancanti, presenti = [], 0
for r in righe:
    if not r or r.startswith("#") or r.startswith(">") or set(r) <= {"-"}:
        continue
    if re.sub(r"\s+", " ", r) in sito_norm:
        presenti += 1
    else:
        mancanti.append(r)

print(f"righe di copy presenti in pagina: {presenti}")
print(f"righe non trovate: {len(mancanti)}")
for m in mancanti:
    print("   NON TROVATA:", repr(m))
sys.exit(0)
