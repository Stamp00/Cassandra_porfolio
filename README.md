# Cassandra Flykt – portfolio

A static portfolio site in English (`/`), Swedish (`/sv/`) and Finnish (`/fi/`), hosted on GitHub Pages.

## Editing text
All text lives in a Google Sheet (its ID is in `build/sheet_id.txt`), one row per text with
English, Swedish and Finnish columns. Edit a cell and the site updates within about 10 minutes:
the "Rebuild pages" GitHub Action downloads the Sheet into `build/content.csv` and rebuilds the pages.
The Sheet must be shared as "Anyone with the link can view".

`build/content.py` holds the original text and is used for anything the Sheet leaves empty.
To rebuild locally: `python3 build/build.py`.

## Files
- `assets/style.css` – design (colours: Silence, Ice Melt, Merlot)
- `assets/main.js` – mobile menu and scroll fade-in
- `assets/img/` – photo and work samples
