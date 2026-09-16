# Ji Pan — English / Deutsch portfolio

Built with Quarto and its Cosmo theme. Requires Quarto and Python 3 (standard library only).

## Preview and build

```sh
quarto preview
quarto render
```

English home: `/index.html`; German home: `/de/index.html`.
The configured output directory is `_site`. If deploying a `docs` folder on GitHub Pages, change `project.output-dir` to `docs`; the localisation hook follows that setting.

## Content layout

| English | German |
|---|---|
| `index.qmd` | `de/index.qmd` |
| `about.qmd` | `de/about.qmd` |
| `experience.qmd` | `de/experience.qmd` |
| `projects.qmd` | `de/projects.qmd` |
| `cv.qmd` | `de/cv.qmd` |

Edit the matching `.qmd` files in both languages, then preview/render normally. Do not edit generated HTML. `de/_metadata.yml` sets the German document language, including Quarto's search and table-of-contents labels.

Quarto uses a shared site navbar. `scripts/localize.py` is a post-render hook that translates the German navigation/footer, highlights the active page/language, and links English/Deutsch to the corresponding page. Links are relative, so they work at localhost, at a domain root, and under a GitHub Pages repository path. The rendered navigation works without JavaScript.

To add a page, create both language files with the same filename, add it to `_quarto.yml`'s navbar, and add its two navigation labels to `LABELS` in `scripts/localize.py`.

## Resume source

Content updated from the German CV dated 2026-09-16. Employment dates are displayed at month precision. The CV records Mercedes-Benz as October 2025–September 2026, English as C1, and German as B2. Only achievements listed in this resume are retained.

Both language versions download `assets/cv/Ji_Pan_CV_DE_2026-09-16.pdf`; the English page explicitly labels this as a German PDF. The older PDF is preserved but is no longer the active download.
