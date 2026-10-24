"""Moves site text between content.py and the Google Sheet (as CSV).

export:  python3 build/sheet.py export build/content.csv   -> writes every text as one row
The build reads build/content.csv (downloaded from the Sheet) and uses it over content.py.
"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import content as C  # noqa: E402

LANGS = ["en", "sv", "fi"]
SKIP = {"path", "html_lang", "label", "menu", "photo_alt", "badge"}

SECTIONS = {
    "title": "Browser tab title", "description": "Google search description",
    "nav": "Menu link", "cta": "Menu button",
    "hello": "Header: greeting", "h1": "Header: headline (text inside <em> is coloured)",
    "tagline": "Header: text under headline", "see_work": "Header: button",
    "showcase_label": "Header: label above work pictures", "showcase": "Header: picture caption",
    "pillars": "Header: four focus areas",
    "brands_label": "Brands row: label",
    "bring_eyebrow": "What I bring: small title", "bring_h2": "What I bring: heading", "bring_lead": "What I bring: intro",
    "tiles": "What I bring: card",
    "work_eyebrow": "Projects: small title", "work_h2": "Projects: heading", "work_lead": "Projects: intro",
    "cases": "Project",
    "writing_label": "I also write: title", "writing": "I also write: item",
    "dir_eyebrow": "Where I'm heading: small title", "dir_quote": "Where I'm heading: quote", "dir_points": "Where I'm heading: point",
    "exp_eyebrow": "Experience: small title", "exp_h2": "Experience: heading", "jobs": "Experience: job", "earlier": "Experience: last line",
    "about_eyebrow": "About: small title", "about_h2": "About: heading", "about": "About: paragraph", "facts": "About: info box",
    "proc_eyebrow": "How I work: small title", "proc_h2": "How I work: heading", "steps": "How I work: step",
    "contact_eyebrow": "Contact: small title", "contact_h2": "Contact: heading", "contact_lead": "Contact: text",
    "linkedin_btn": "Contact: LinkedIn button", "email_btn": "Contact: email button", "footer": "Footer text",
}
PART_NAMES = {
    "tiles": ["title", "text"], "dir_points": ["title", "text"], "facts": ["title", "text"], "steps": ["title", "text"],
    "showcase": ["bold part", "rest"], "jobs": ["job title", "employer", "dates", "description"],
}


def flatten(value, path):
    if isinstance(value, str):
        yield path, value
    elif isinstance(value, dict):
        for k, v in value.items():
            yield from flatten(v, path + [k])
    elif isinstance(value, (list, tuple)):
        for i, v in enumerate(value, 1):
            yield from flatten(v, path + [str(i)])


def label(path):
    top = path[0]
    name = SECTIONS.get(top, top)
    rest = path[1:]
    if top in PART_NAMES and len(rest) == 2:
        return f"{name} {rest[0]}: {PART_NAMES[top][int(rest[1]) - 1]}"
    if top == "cases" and rest:
        return f"{name} {rest[0]}: " + " ".join(rest[1:])
    return f"{name} {' '.join(rest)}".strip()


def rows():
    base = C.CONTENT["en"]
    order = list(SECTIONS) + [k for k in base if k not in SECTIONS]
    for key in order:
        if key in SKIP or key not in base:
            continue
        for path, en in flatten(base[key], [key]):
            vals = []
            for lang in LANGS:
                v = C.CONTENT[lang]
                for p in path:
                    v = v[int(p) - 1] if isinstance(v, (list, tuple)) else v[p]
                vals.append(v)
            yield ".".join(path), label(path), vals
    yield "settings.linkedin", "Settings: LinkedIn link", [C.LINKEDIN, "", ""]
    yield "settings.email", "Settings: email (leave empty to hide)", [C.EMAIL or "", "", ""]
    yield "settings.brands", "Settings: brands row (comma separated)", [", ".join(C.BRANDS), "", ""]


def export(out):
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["What it is", "English", "Swedish", "Finnish", "ID (don't edit)"])
        for key, lab, vals in rows():
            w.writerow([lab, *vals, key])


def _set(obj, path, value):
    """Set value at path, turning tuples into lists on the way."""
    parent, last = obj, path[-1]
    chain = []
    for p in path[:-1]:
        chain.append((parent, p))
        parent = parent[int(p) - 1] if isinstance(parent, (list, tuple)) else parent[p]
    if isinstance(parent, tuple):
        new = list(parent)
        new[int(last) - 1] = value
        gp, gk = chain[-1]
        if isinstance(gp, list):
            gp[int(gk) - 1] = new
        else:
            gp[gk] = new
    elif isinstance(parent, list):
        parent[int(last) - 1] = value
    else:
        parent[last] = value


def apply_csv(path):
    """Overrides content.py with the text in the Sheet's CSV. Unknown or empty cells are ignored."""
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        cols = {name.strip().lower(): i for i, name in enumerate(header)}
        idc = next(i for n, i in cols.items() if n.startswith("id"))
        lc = [cols["english"], cols["swedish"], cols["finnish"]]
        for row in reader:
            if len(row) <= idc or not row[idc].strip():
                continue
            key = row[idc].strip()
            vals = [row[i].strip() if i < len(row) else "" for i in lc]
            if key.startswith("settings."):
                name = key.split(".", 1)[1]
                if name == "linkedin" and vals[0]:
                    C.LINKEDIN = vals[0]
                elif name == "email":
                    C.EMAIL = vals[0] or None
                elif name == "brands" and vals[0]:
                    C.BRANDS = [b.strip() for b in vals[0].split(",") if b.strip()]
                continue
            p = key.split(".")
            for lang, v in zip(LANGS, vals):
                if not v:
                    continue
                try:
                    _set(C.CONTENT[lang], p, v)
                except (KeyError, IndexError, ValueError):
                    print(f"skipped unknown row {key}")


if __name__ == "__main__" and sys.argv[1:2] == ["export"]:
    export(sys.argv[2])
