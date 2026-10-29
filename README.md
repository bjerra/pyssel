# Craft Kids

Draft static website of craft projects for children aged 9–12, written in Swedish.

Each project page rewrites the instructions in our own words and credits the original source. The about page lists those sources.

## Preview locally

From this directory:

```bash
python3 -m http.server
```

Then open http://localhost:8000/

## Search engines

This draft is not published for search. Every page sends `noindex, nofollow`, and `robots.txt` disallows all crawlers.

## Files

- `index.html`, `pyssel.html`, `om.html` — home, full list, and about
- `projects/` — one page for each of the 17 crafts
- `assets/style.css` — shared stylesheet
- `catalogue.json` — project catalogue
- `build/` — `content.py` and `gen.py`, used to regenerate the pages (`python3 build/gen.py`)
- `shortlist.md` and `halloween-shortlist.md` — the working shortlists
