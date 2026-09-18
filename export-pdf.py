"""Print the deck to PDF with headless Chrome.

    python export-pdf.py                # talk slides only -> ICAI2026-slides.pdf
    python export-pdf.py --with-backup  # also the hidden backup slides

Builds a static print page (one fixed 1920x1080 page per slide, same
css/theme.css, footer and page numbers baked in) and prints it with Chrome.
This avoids reveal.js' ?print-pdf mode, which is unreliable headless.
"""
import os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
WITH_BACKUP = "--with-backup" in sys.argv
OUT = os.path.join(HERE, "ICAI2026-slides-with-backup.pdf" if WITH_BACKUP else "ICAI2026-slides.pdf")
FOOTER = "ICAI 2026 · Universidad de los Andes"

CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    shutil.which("google-chrome") or "", shutil.which("chromium") or "",
]
CHROME = next((c for c in CANDIDATES if c and os.path.exists(c)), None)
if not CHROME:
    sys.exit("Chrome/Edge not found; open index.html?print-pdf in Chrome and print manually.")

html = open(os.path.join(HERE, "index.html"), encoding="utf-8").read()
fonts = re.search(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^"]*">', html).group(0)
sections = re.findall(r"<section\b.*?</section>", html, flags=re.S)
visible = [s for s in sections if 'data-visibility="hidden"' not in s]
pages = sections if WITH_BACKUP else visible
total = len(visible)

body = []
for i, s in enumerate(pages, 1):
    hidden = 'data-visibility="hidden"' in s
    num = f"backup {i - total}" if hidden else f"{i} / {total}"
    footer = f'<div class="pfoot">{FOOTER}</div><div class="pnum">{num}</div>'
    s = re.sub(r"<aside class=\"notes\">.*?</aside>", "", s, flags=re.S)
    s = s.replace("</section>", footer + "</section>")
    body.append(s)

PRINT_CSS = """
*{margin:0;box-sizing:border-box} @page{size:1920px 1080px;margin:0} html,body{background:#fff}
section{position:relative;width:1920px;height:1080px;overflow:hidden;page-break-after:always;break-after:page}
section:last-of-type{page-break-after:auto}
.pfoot,.pnum{position:absolute;bottom:64px;font-family:'IBM Plex Mono','Courier New',monospace;font-size:24px;color:#8a8f99}
.pfoot{left:128px} .pnum{right:128px}
.slide.centered ~ .pfoot, .slide.centered ~ .pnum{display:none}
"""
doc = (f'<!doctype html><html><head><meta charset="utf-8"><title>ICAI 2026</title>{fonts}'
       f'<link rel="stylesheet" href="css/theme.css"><style>{PRINT_CSS}</style></head>'
       f'<body><div class="reveal"><div class="slides">{"".join(body)}</div></div></body></html>')
src = os.path.join(HERE, "_print.html")
open(src, "w", encoding="utf-8").write(doc)

profile = tempfile.mkdtemp(prefix="deck-pdf-")
cmd = [CHROME, "--headless=new", "--disable-gpu", f"--user-data-dir={profile}",
       "--no-pdf-header-footer", "--virtual-time-budget=20000",
       "--run-all-compositor-stages-before-draw", f"--print-to-pdf={OUT}",
       "file:///" + src.replace(os.sep, "/")]
subprocess.run(cmd, check=False, capture_output=True, timeout=240)
os.remove(src)
shutil.rmtree(profile, ignore_errors=True)
ok = os.path.exists(OUT) and os.path.getsize(OUT) > 10_000
print(("OK" if ok else "FAILED"), OUT, f"({len(pages)} slides)")
