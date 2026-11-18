# news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/ginoray/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/ginoray/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

One picture that sums up the world's news of **Wednesday, 18 November 2026**: the APEC summit in Shenzhen as the lead story, with eight cards — the US strike on Iran's Qeshm Island and Iran's drone answer, the Kerch Bridge strike, Alaska's Senate flip, the US losing its measles-free status, DR Congo's Ebola outbreak, the EU's clean-energy permitting deal, the markets' Nvidia day, and GTA VI's midnight launch — plus an "also today" strip (Cyclone Xavier, the Siberia plane crash, Gaza's cold). Every headline was cross-checked against at least two independent reports published that day.

The program decodes the poster (kept base64-encoded in `assets/entry.png.b64`, so the repository stays plain text end to end), validates it against the bounty's limits (a whole PNG, ≤ 1 MiB, ≤ 1024×1024) and writes it, byte for byte, to `/output/entry.png`. The poster is rendered by `tools/build_image.py` (Pillow), which is kept in the repo so the picture can be rebuilt and audited; the shipped program itself uses only the Python standard library and no network.

## Run it

```sh
python3 main.py
```

---
<sub>Entered on [make.fun](https://make.fun/?ref=ginoray&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
