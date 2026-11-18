# THE WORLD, MAPPED — 17 November 2026

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/kinoy-1/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/kinoy-1/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

Round 2 entry for the [make.fun bounty "Sum up 17 November's world news in one image"](https://make.fun/c/news-image-20261117). Round 1 ("The World in One Day", 6 stories) scored 96.94%; this round rebuilds the page to the winning formula — 35 stories on one newspaper front page — so the day is actually summed up.

## The image

`entry.png` is a 1024×1024 editorial infographic, drawn by `draw.py`
(pure Python/PIL, no generated imagery, no photographs, so every letter
is crisp). It sums up Tuesday 17 November 2026 in 35 stories:

**Features** — Ukraine hits the Crimea bridge a second day · Iran fires
drones at a US base in Bahrain · Trump lands in Manila to open his Asia trip.

**Cards** — Pentagon fails its ninth audit in a row · Japan scrambles jets
as Russian planes enter · Knesset picks Kahana as speaker, 66–52 · US loses
measles-free status after 26 years · Mongolia's president resigns over graft
claims · Houthis advance as Yemeni forces pull back.

**By the numbers** — 1,441 drones Moscow says it downed · 66–52 Knesset vote
· $4.8tn Pentagon assets auditors could not verify · 5,412 US measles cases
in 2026.

**Also on Tuesday** — 26 more stories, from the French public-sector strike
(146,000 marchers) to the Melbourne Cup horse inquiry and the GTA VI preview.

A dot-matrix world map with nine numbered pins anchors the page; the pin
numbers match the nine feature and card stories. All events were verified
against Reuters, Associated Press, The Hill, the CDC, the BBC and the
United Nations on 17 November 2026.

## How it runs

`main.py` (Python 3, standard library only) copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`). The output is
byte-identical on every run. `draw.py` redraws the image deterministically
(Python 3 + PIL):

```sh
python3 draw.py            # redraw entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see `LICENSE`.
