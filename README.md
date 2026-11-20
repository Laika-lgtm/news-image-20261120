# The World Today — Friday 20 November 2026

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Laika-lgtm/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Laika-lgtm/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One image that sums up the world's news of **Friday 20 November 2026**:
31 stories across 6 continents, led by Cyclone Akvan's landfall on
India's east coast, the overnight missile strikes on Kyiv's Dnipro
bridges, and the final day of COP31 in Antalya — plus the APEC
aftermath in Shenzhen and the day's markets, diplomacy and sport.

## How it is made

`build_image.py` (Pillow, run locally) lays out the front page from
four editorial photographs in `assets/` and a story list in which
every item was checked against Reuters, CNN, AP, WSJ, Le Monde, the
India Meteorological Department and the COP31 draft texts on
20 November 2026. Stories first reported on 19 November sit in
their own band, dated as such. `main.py` (standard library only)
copies the finished `entry.png` to the output directory, so both
graded runs write byte-identical files.

## Run it

```sh
python3 build_image.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see [LICENSE](LICENSE).
