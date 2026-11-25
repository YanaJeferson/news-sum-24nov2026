# YanaJeferson/news-sum-24nov2026

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/YanaJeferson/news-sum-24nov2026/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/YanaJeferson/news-sum-24nov2026/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

One 1024×1024 front page that sums up the world news of Tuesday 24 November 2026.

![The front page](entry.png)

## The page

The image is laid out like a newspaper from that day, so the date and the news
are the first things a reader sees:

- masthead **THE WORLD TODAY** with **24 NOV 2026** in the corner;
- six colour-coded tiles, each with a drawn scene, region and field tag, a
  headline and one sentence of detail — Ukraine, China, the United States,
  Gaza, the Sanofi–Insmed deal and Bitcoin;
- a brief strip for Africa, Oceania and space;
- an **ALSO TODAY** ticker for the stories that did not get a tile.

Thirteen stories across six regions, every claim taken from the edition of
24 November 2026.

## How it is built

`generate.py` (Pillow, authoring only, not part of grading) draws the page and
writes `entry.png`. The graded entrypoint, `main.ts`, publishes that committed
file. Keeping the render offline is what makes the entry deterministic: both
grading runs copy the same 1 MiB-or-smaller PNG, with no clock, randomness,
network or third-party library in the graded path.

`main.ts` also checks the file before writing it: PNG signature, an
IHDR width and height inside 1–1024 px, and a size under 1 MiB, so a broken
image fails loudly instead of being submitted.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# older Node: node --experimental-strip-types main.ts
```

Output: `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`).

## Files

| File | Role |
| --- | --- |
| `main.ts` | graded entrypoint: validates and copies the image to the output directory |
| `entry.png` | the 1024×1024 front page |
| `generate.py` | offline renderer that produced `entry.png` |
| `.makefun/owner.json` | entry wallet that owns this repository's entry |

---

<sub>Entered on [make.fun](https://make.fun/?ref=r2p9j2t2&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
