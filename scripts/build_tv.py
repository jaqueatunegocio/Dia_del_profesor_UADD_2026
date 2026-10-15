"""Genera tv/index.html (presentación para TV) a partir de index.html.

Uso:  python3 scripts/build_tv.py
Vuelve a ejecutarlo cada vez que cambie el contenido de la página principal.
"""
import json
import pathlib
import re

from bs4 import BeautifulSoup

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://diadelprofesoruadd2026.vercel.app/"


def txt(el):
    return re.sub(r"\s+", " ", el.get_text(" ", strip=True)).replace(" ,", ",").replace(" .", ".") if el else ""


def html_inner(el):
    """Texto conservando <strong> (nombres de proyectos)."""
    if not el:
        return ""
    out = []
    for p in el.find_all("p") or [el]:
        out.append("".join(str(c) for c in p.contents))
    return " ".join(out).strip()


def asset(src):
    return BASE + src if src and not src.startswith("http") else src


def person(t):
    img = t.select_one("img")
    return {
        "name": txt(t.select_one("h4")),
        "school": txt(t.select_one(".school")),
        "photo": asset(img["src"]) if img else None,
    }


def main():
    s = BeautifulSoup((ROOT / "index.html").read_text(encoding="utf-8"), "html.parser")
    slides = [{"type": "video", "src": BASE + "video/saludo-director.mp4", "poster": BASE + "img/saludo-poster.jpg"}]

    th = s.select_one(".thanks")
    paras = [html_inner(p) for p in th.select("p")]
    slides.append({"type": "cover", "eyebrow": txt(th.select_one(".eyebrow")), "paras": paras})

    sec = s.select_one(".section")
    slides.append({"type": "intro", "eyebrow": txt(sec.select_one(".eyebrow")),
                   "title": txt(sec.select_one("h2")), "text": txt(sec.select_one(".intro"))})

    for n, d in enumerate(s.select("details.category"), 1):
        cat = txt(d.select_one("h3"))
        icon = txt(d.select_one(".icon"))
        slides.append({"type": "category", "num": f"{n:02d}", "icon": icon, "title": cat,
                       "text": txt(d.select_one(".description"))})
        cards = d.select(".story-card")
        if cards:
            for c in cards:
                ach = c.select_one(".achievements")
                slides.append({
                    "type": "story", "cat": cat, "icon": icon,
                    "label": txt(c.select_one(".field-label")),
                    "title": txt(c.select_one("h4")),
                    "people": [person(t) for t in c.select("article.teacher")],
                    "quote": html_inner(c.select_one(".quote")),
                    "achievements": html_inner(ach) if ach else "",
                })
        else:
            for t in d.select("article.teacher"):
                p = person(t)
                desc = t.select_one(".teacher-desc")
                slides.append({"type": "teacher", "cat": cat, "icon": icon, **p,
                               "quote": html_inner(desc) if desc else ""})

    cl = s.select_one(".closing")
    slides.append({"type": "closing", "title": txt(cl.select_one("h2")),
                   "text": txt(cl.select_one("p")), "final": txt(cl.select_one("strong"))})

    tpl = (ROOT / "scripts" / "tv_template.html").read_text(encoding="utf-8")
    out = tpl.replace("/*__SLIDES__*/[]", json.dumps(slides, ensure_ascii=False))
    (ROOT / "tv").mkdir(exist_ok=True)
    (ROOT / "tv" / "index.html").write_text(out, encoding="utf-8")
    print(f"tv/index.html generado con {len(slides)} slides")


if __name__ == "__main__":
    main()
