# Yisheng He's personal website

A static academic homepage for GitHub Pages. No build step or JavaScript runtime is required.

## Local preview

From the repository root, run:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Open `http://127.0.0.1:8000` in a browser. `index.html` contains the content; `stylesheet.css` contains the shared desktop and mobile styles.

## Updating publications

- Copy one `article.publication` inside the Research section and keep its `id`, heading `id`, and `aria-labelledby` unique and consistent.
- Add the title, authors, venue, verified resource links, and a short description. Use real URLs; omit unavailable links until they are public.
- Keep original figures in `images/`. Display an optimized thumbnail and link it to the original figure. Supply accurate `alt` text and the thumbnail's intrinsic `width` and `height`; CSS preserves its aspect ratio.
- Use `loading="lazy"` and `decoding="async"` for figures below the first publication. Keep the portrait and first publication image eager.
- Update the footer date and review the result at desktop and mobile widths.

Recent figures include `images/lambda0.webp`, `images/egoalign.webp`, and `images/past-as-state.webp`. The λ₀ thumbnail shows the HumanVerse panel from Figure 1 on page 1 of [the report](https://arxiv.org/pdf/2610.18950); it links to the complete figure in `images/lambda0-overview.webp`. EgoAlign links to `images/egoalign-pipeline.webp` for its full diagram.

## Regenerating older thumbnails

Install Pillow in your Python environment, then run:

```sh
python3 scripts/optimize_thumbnails.py
```

The script preserves complete figures and aspect ratios, never enlarges an image, and writes WebP files under `images/thumbnails/` with a maximum width of 480 pixels. It leaves originals untouched. Add a source to `SOURCES` when extending this batch; copy the generated dimensions into its HTML image attributes.

The optional `--manifest /tmp/thumbnails.json` argument writes source paths, output paths, dimensions, and byte counts for verification.

## Hosting and external resources

The canonical URL and sharing metadata use `https://hyshkust.github.io/`. Keep them aligned if the domain changes. Lato fonts use Google Fonts with `font-display: swap`; GitHub star badges use Shields.io and load lazily. The page content and links work without JavaScript.
