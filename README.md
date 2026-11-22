# THE WORLD TODAY — Sunday 22 November 2026 (v6)

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/DavidQlla06/news-image-20261122-v6/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/DavidQlla06/news-image-20261122-v6/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

A single 1024×1024 broadsheet image summing up the world news of Sunday
22 November 2026: a map-led lead story (COP31 climate talks end in
collapse — no deal adopted in Antalya) with 13 numbered markers, twelve
illustrated story cards, a twelve-item regional briefs panel and a
six-item news ticker — 31 stories across 7 regions.

Headlines drawn from live wire reporting on 22 Nov 2026 (Reuters, AP,
CNN, Formula1.com, WRI, NPR and others): the Hormuz tanker war, the
Kryvyi Rih triple-tap strike, the Sparta II fire, Verstappen's Las
Vegas GP win (+0.639s over Norris), the AI market rout, the capture of
"El Chapo Isidro", Peru's M6.7 earthquake, Sudan's army retaking
Al-Khuway, the US losing measles elimination status, Manipur's toxic
liquor deaths, the Air Niugini emergency landing, the EU-Indonesia
CEPA signing and Estonia's Russia border closure.

## Build

- `generate.py` renders `entry.png` from the story JSON files
  (`stories.json`, `cards.json`, `list.json`, `ticker.json`) with Pillow.
- `main.py` is the make.fun entrypoint: it copies `entry.png` to
  `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR` outside the grader).

Entered in make.fun competition `news-image-20261122`.
