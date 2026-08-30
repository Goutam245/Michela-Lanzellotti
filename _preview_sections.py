# -*- coding: utf-8 -*-
"""Strumento di sviluppo: genera una pagina statica per ogni sezione,
così da poterle fotografare una alla volta senza dipendere dallo scorrimento."""
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "public", "index.html")
OUT = os.path.join(ROOT, "public", "_sez")
os.makedirs(OUT, exist_ok=True)

html = open(SRC, encoding="utf-8").read()

head = re.search(r"<head>(.*?)</head>", html, re.S).group(1)
sprite = re.search(r'(<svg width="0" height="0".*?</svg>)', html, re.S).group(1)
main = re.search(r"<main id=\"contenuto\">(.*?)</main>", html, re.S).group(1)
footer = re.search(r"(<footer class=\"site-footer\">.*?</footer>)", html, re.S).group(1)

# i percorsi risalgono di un livello
def up(t):
    t = t.replace('href="assets/', 'href="../assets/').replace('src="assets/', 'src="../assets/') \
         .replace('href="index.html', 'href="../index.html').replace('href="informativa.html', 'href="../informativa.html')
    # anche le sorgenti multiple vanno risalite di un livello
    t = re.sub(r'((?:image)?srcset=")([^"]+)"', lambda m: m.group(1) + m.group(2).replace('assets/', '../assets/') + '"', t)
    return t

sezioni = re.findall(r'(<section\b[^>]*>.*?</section>)', main, re.S)
indice = []

for i, sez in enumerate(sezioni, start=1):
    m = re.search(r'id="([\w-]+)"', sez)
    sid = m.group(1) if m else f"sez{i}"
    pagina = f"""<!doctype html>
<html lang="it" class="anteprima">
<head>{up(head)}
<link rel="stylesheet" href="_anteprima.css">
<style>
  body {{ padding-top: 0 !important; }}
  .hero {{ padding-top: 3rem !important; }}
  .band, .maisons {{ padding-block: 3.5rem !important; }}
</style>
</head>
<body>
{sprite}
<main>
{up(sez)}
</main>
</body>
</html>
"""
    with open(os.path.join(OUT, f"{i:02d}-{sid}.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(pagina)
    indice.append(f"{i:02d}-{sid}.html")

# piè di pagina a sé
with open(os.path.join(OUT, "99-footer.html"), "w", encoding="utf-8", newline="\n") as f:
    f.write(f"<!doctype html>\n<html lang=\"it\" class=\"anteprima\">\n<head>{up(head)}</head>\n<body>\n{sprite}\n{up(footer)}\n</body>\n</html>\n")
indice.append("99-footer.html")

print("\n".join(indice))
