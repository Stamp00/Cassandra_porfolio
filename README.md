# Cassandra Flykt – portfolio

A static portfolio site in English (`/`), Swedish (`/sv/`) and Finnish (`/fi/`), hosted on GitHub Pages.

## Editing text
All text lives in `build/content.py`. After editing, rebuild the pages:

```
python3 build/build.py
```

Then commit the changed `index.html`, `sv/index.html` and `fi/index.html`.

## Files
- `assets/style.css` – design (colours: Silence, Ice Melt, Merlot)
- `assets/main.js` – mobile menu and scroll fade-in
- `assets/img/` – photo and work samples
