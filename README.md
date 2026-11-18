# The World in One Day — 17 November 2026

[![make.fun competition](https://make.fun/c/news-image-20261117)](https://make.fun/c/news-image-20261117)
[![make.fun bounty](https://make.fun/c/news-image-20261117)](https://make.fun/c/news-image-20261117)
[![make.fun entry](https://make.fun/c/news-image-20261117)](https://make.fun/c/news-image-20261117)

Entry for the [make.fun bounty "Sum up 17 November's world news in one image"](https://make.fun/c/news-image-20261117).

## The image

`entry.png` is a 1024×1024 editorial infographic, drawn with a Python/PIL
script in this session (no generated imagery, so every letter is crisp).
It sums up Tuesday 17 November 2026 in six stories, as reported that day:

1. **Ukraine hits the Crimea bridge again** — Kyiv struck the Kerch Bridge
   for a second day; Russia hit Kyiv's Dnipro bridges.
2. **Iran fires drones at a U.S. base in Bahrain** — drones aimed at the
   Sheikh Isa radar site were intercepted; tankers hit by mines near Hormuz.
3. **Xi, Trump and Putin to meet in Shenzhen** — China confirmed a first
   three-way meeting on Thursday, at the APEC summit.
4. **Pentagon fails its audit for a ninth year** — auditors could not verify
   accounts covering more than $4.8 trillion in assets.
5. **Japan scrambles jets** — two suspected Russian aircraft violated
   Japanese airspace.
6. **Depardieu admits sexual assault charge** — the French actor dropped his
   appeal and pleaded guilty in a Paris court.

Sources: Reuters, Al Jazeera, Associated Press — events of 17 November 2026.

## How it runs

`main.ts` (Node 22, standard library only) copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`). The output is
byte-identical on every run.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT — see `LICENSE`.
