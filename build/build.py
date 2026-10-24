"""Builds index.html (English), sv/index.html and fi/index.html from content.py.

Run from the repo root:  python3 build/build.py
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from content import CONTENT, BRANDS, LINKEDIN, EMAIL  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SITE_URL = ""  # set to e.g. "https://cassandraflykt.com" once the domain is live

ARROW = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M8 7h9v9"/></svg>'

TILE_STYLES = ["ice wide", "merlot", "", "blush", "ice"]


def case_media(i, a):
    img = lambda f, cls="", alt="": f'<img src="{a}img/{f}" class="{cls}" alt="{alt}" loading="lazy">'
    if i == 0:
        return f'''<div class="case-media combo">
          <div class="browser">{img("peppar-website.webp", alt="pepparcatering.fi")}</div>
          {img("peppar-instagram.webp", "phone", "Peppar Catering Instagram")}
        </div>'''
    if i == 1:
        return f'''<div class="case-media ice">
          {img("pohjola-instagram.webp", "phone", "Pohjola-Norden Instagram")}
          {img("nordjobb-reel.webp", "phone", "Nordjobb reel")}
        </div>'''
    return f'''<div class="case-media blush combo">
          <div style="display:grid;gap:16px">{img("blog-hitachi.webp", alt="Hitachi Energy customer story")}{img("blog-spot.webp", alt="Spot app article")}</div>
          {img("creo-linkedin.webp", "phone", "Creo Center LinkedIn")}
        </div>'''


def page(lang):
    t = CONTENT[lang]
    a = "../assets/" if t["path"] else "assets/"
    home = "../" if t["path"] else ""
    ids = ["work", "about", "experience", "contact"]

    langs = "".join(
        f'<a href="{home}{c["path"]}" hreflang="{c["html_lang"]}" aria-current="{str(k == lang).lower()}">{c["label"]}</a>'
        for k, c in CONTENT.items()
    )
    alternates = "\n".join(
        f'  <link rel="alternate" hreflang="{c["html_lang"]}" href="{SITE_URL}/{c["path"]}">' for c in CONTENT.values()
    ) if SITE_URL else ""
    nav = "".join(f'<a href="#{i}">{n}</a>' for i, n in zip(ids, t["nav"]))
    pillars = "".join(f"<div><small>0{n}</small>{p}</div>" for n, p in enumerate(t["pillars"], 1))
    brands = "".join(f"<li>{b}</li>" for b in BRANDS)
    tiles = "".join(
        f'<div class="tile {s} reveal"><span class="num">0{n}</span><h3>{h}</h3><p>{p}</p></div>'
        for n, ((h, p), s) in enumerate(zip(t["tiles"], TILE_STYLES), 1)
    )
    cases = "".join(
        f'''<article class="case reveal">
        <div>
          {"".join(f'<span class="tag">{g}</span>' for g in c["tags"])}
          <h3>{c["title"]}</h3>
          <div class="client">{c["client"]}</div>
          <p class="body">{c["body"]}</p>
          <ul>{"".join(f"<li>{p}</li>" for p in c["points"])}</ul>
        </div>
        {case_media(i, a)}
      </article>'''
        for i, c in enumerate(t["cases"])
    )
    writing = "".join(f"<span>{w}</span>" for w in t["writing"])
    dir_points = "".join(f"<div><strong>{h}</strong><p>{p}</p></div>" for h, p in t["dir_points"])
    jobs = "".join(
        f'<div class="job reveal"><div><div class="role">{r}</div><div class="org">{o}</div></div><p>{d}</p><span class="when">{w}</span></div>'
        for r, o, w, d in t["jobs"]
    )
    about = "".join(f"<p>{p}</p>" for p in t["about"])
    facts = "".join(f"<div><strong>{h}</strong><span>{p}</span></div>" for h, p in t["facts"])
    steps = "".join(f'<div class="step reveal"><h3>{h}</h3><p>{p}</p></div>' for h, p in t["steps"])
    email_btn = f'<a class="btn ghost" href="mailto:{EMAIL}">{t["email_btn"]}<span class="dot">{ARROW}</span></a>' if EMAIL else ""
    canonical = f'<link rel="canonical" href="{SITE_URL}/{t["path"]}">' if SITE_URL else ""
    og_image = f'<meta property="og:image" content="{SITE_URL}/assets/img/cassandra.webp">' if SITE_URL else ""

    return f'''<!doctype html>
<html lang="{t["html_lang"]}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{t["title"]}</title>
  <meta name="description" content="{t["description"]}">
  <meta property="og:title" content="{t["title"]}">
  <meta property="og:description" content="{t["description"]}">
  <meta property="og:type" content="website">
  {og_image}
  {canonical}
{alternates}
  <meta name="theme-color" content="#fdfbf7">
  <link rel="icon" href="{a}favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{a}style.css">
</head>
<body>
  <header class="header">
    <div class="wrap">
      <a class="logo" href="#top">Cassandra Flykt<span>.</span></a>
      <nav class="nav" id="nav">
        {nav}
        <div class="lang" aria-label="Language">{langs}</div>
      </nav>
      <button class="menu-btn" aria-expanded="false" aria-controls="nav" aria-label="{t["menu"]}">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
      </button>
    </div>
  </header>

  <main id="top">
    <section class="hero">
      <div class="wrap">
        <div class="hero-card">
          <div>
            <p class="hello">{t["hello"]}</p>
            <h1>{t["h1"]}</h1>
            <p class="tagline"><strong>{t["role"]}</strong> {t["tagline"]}</p>
            <div class="actions">
              <a class="btn" href="#work">{t["see_work"]}<span class="dot">{ARROW}</span></a>
              <a class="btn light" href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn<span class="dot">{ARROW}</span></a>
            </div>
          </div>
          <div class="portrait">
            <img src="{a}img/cassandra.webp" alt="{t["photo_alt"]}" width="489" height="489">
            <span class="badge"><i></i>{t["badge"]}</span>
          </div>
          <div class="pillars">{pillars}</div>
        </div>
      </div>
    </section>

    <section class="brands" aria-label="{t["brands_label"]}">
      <div class="wrap">
        <p>{t["brands_label"]}</p>
        <ul>{brands}</ul>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="head reveal">
          <div><span class="eyebrow">{t["bring_eyebrow"]}</span><h2>{t["bring_h2"]}</h2></div>
          <p class="lead">{t["bring_lead"]}</p>
        </div>
        <div class="bento">{tiles}</div>
      </div>
    </section>

    <section class="section" id="work" style="padding-top:0">
      <div class="wrap">
        <div class="head reveal">
          <div><span class="eyebrow">{t["work_eyebrow"]}</span><h2>{t["work_h2"]}</h2></div>
          <p class="lead">{t["work_lead"]}</p>
        </div>
        <div class="cases">{cases}</div>
        <div class="reveal" style="margin-top:40px">
          <span class="eyebrow">{t["writing_label"]}</span>
          <div class="writing">{writing}</div>
        </div>
      </div>
    </section>

    <section style="padding-bottom:clamp(64px,10vw,120px)">
      <div class="wrap">
        <div class="direction reveal">
          <div>
            <span class="eyebrow">{t["dir_eyebrow"]}</span>
            <blockquote>{t["dir_quote"]}</blockquote>
          </div>
          <div class="points">{dir_points}</div>
        </div>
      </div>
    </section>

    <section class="section" id="experience" style="padding-top:0">
      <div class="wrap">
        <div class="head reveal"><div><span class="eyebrow">{t["exp_eyebrow"]}</span><h2>{t["exp_h2"]}</h2></div></div>
        <div class="jobs">{jobs}</div>
        <p style="margin-top:20px;color:var(--muted);font-size:.95rem">{t["earlier"]}</p>
      </div>
    </section>

    <section class="section" id="about" style="padding-top:0">
      <div class="wrap about">
        <div class="photo reveal"><img src="{a}img/cassandra.webp" alt="{t["photo_alt"]}" loading="lazy"></div>
        <div class="text reveal">
          <span class="eyebrow">{t["about_eyebrow"]}</span>
          <h2 style="margin-bottom:20px">{t["about_h2"]}</h2>
          {about}
          <div class="facts">{facts}</div>
        </div>
      </div>
    </section>

    <section class="section" style="padding-top:0">
      <div class="wrap">
        <div class="head reveal"><div><span class="eyebrow">{t["proc_eyebrow"]}</span><h2>{t["proc_h2"]}</h2></div></div>
        <div class="steps">{steps}</div>
      </div>
    </section>

    <section id="contact">
      <div class="wrap">
        <div class="contact reveal">
          <span class="eyebrow">{t["contact_eyebrow"]}</span>
          <h2>{t["contact_h2"]}</h2>
          <p class="lead">{t["contact_lead"]}</p>
          <div class="actions">
            <a class="btn" href="{LINKEDIN}" target="_blank" rel="noopener">{t["linkedin_btn"]}<span class="dot">{ARROW}</span></a>
            {email_btn}
          </div>
        </div>
      </div>
    </section>
  </main>

  <footer class="footer">
    <div class="wrap"><span>© 2026 Cassandra Flykt</span><span>{t["footer"]}</span></div>
  </footer>
  <script src="{a}main.js"></script>
</body>
</html>
'''


if __name__ == "__main__":
    for lang, t in CONTENT.items():
        out = ROOT / t["path"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page(lang), encoding="utf-8")
        print("wrote", out.relative_to(ROOT))
