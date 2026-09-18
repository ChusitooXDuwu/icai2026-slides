# ICAI 2026 — Domain-Adapted SLMs for Course-Aware Automated Feedback

**Live deck:** https://chusitooxduwu.github.io/icai2026-slides/

Slides for the ICAI 2026 talk on *Domain-Adapted Small Language Models for
Course-Aware Automated Feedback in Introductory Programming*
(Rosales, Chu, Manrique, Sánchez — Universidad de los Andes).

Built with [reveal.js](https://revealjs.com) loaded from a CDN: no build step,
no dependencies. Open `index.html` in a browser and present.

## Files

| File | What it is |
|---|---|
| `index.html` | The deck. One `<section>` per slide, in order. |
| `css/theme.css` | The look (colours, type, reusable blocks: tiles, cards, code panels, pipeline, stats). |
| `img/fig1-results.png` | Figure 1 of the paper (human evaluation by model and criterion). |
| `export-pdf.py` | Prints the deck to PDF with headless Chrome. |

## Presenting

- Open `index.html` (double-click, or serve the folder with `python -m http.server`).
- `S` opens the speaker view with notes and timer. `F` = fullscreen, `Esc` = overview, `?` = all shortcuts.
- Slides are authored at 1920×1080 and scale to any screen.

## Editing

Each slide is a `<section>` wrapping one `<div class="slide">`:

```html
<section data-transition="fade">
  <div class="slide">
    <div class="head"><p class="eyebrow">03 · The gap</p><h2>Slide title</h2></div>
    ... content ...
  </div>
  <aside class="notes">Speaker notes (shown in the S view only).</aside>
</section>
```

Reusable blocks (all defined in `css/theme.css`):

- `.row` / `.grid2` — columns; `.tile` (big number + label), `.stat` (result number), `.card` (bordered box, `hi` = blue highlight).
- `.code` — code panel; one `<p>` per line, indent with `&nbsp;`, `.kw` for keywords, `.cm` for comments.
- `.pills` + `.pill` — inline tags; `.numbered` — 1-2-3 list; `.pipeline` — inputs → model → output.
- Text: `.lead` (30px), `.note` (26px grey), `.small` (24px grey), `.rq` (blue statement).

Hidden backup slides carry `data-visibility="hidden"`: they are skipped when presenting
and not counted in the page numbers. Delete the attribute to show one.

Vertical budget per slide: 1080 px minus 128 top / 160 bottom = 792 px of content.
If a slide overflows, split it; nothing shrinks automatically.

## PDF

- In Chrome: open `index.html?print-pdf`, then Print → Save as PDF, landscape, no margins, background graphics on.
- Or run `python export-pdf.py` (needs Chrome installed) → `ICAI2026-slides.pdf`.
  Add `--with-backup` to include the hidden slides.

## Publishing on the web

The repo is served with GitHub Pages from the `main` branch root, so the deck is
live at **https://chusitooxduwu.github.io/icai2026-slides/** (source: https://github.com/ChusitooXDuwu/icai2026-slides). Every push updates it within a minute.
