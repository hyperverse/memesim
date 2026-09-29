# Recall exchange, 1000 generations

Date: 2026-09-29. Log: `logs/memesim_20260929_153252.log` (not committed; `logs/` is gitignored).

Grid 30×30 (900 agents, 4500 slots), meme length 16, pool size 5, hearing flip rate 0.02, mismatch threshold 0.25. Each generation an agent hears one neighbor's broadcast. A hearing within 4 bits strengthens the closest slot and leaves its bits unchanged. A farther hearing copies the heard string onto the weakest slot at strength 1. The agent broadcasts the slot that hearing selected.

## What the log shows

| Generation | Unique patterns | Strengthen / write | Mean broadcast strength | Strength of the slots that matched |
|---|---|---|---|---|
| 0 | 4330 | — | — | — |
| 50 | 2442 | 478 / 422 | 4.2 | 7 |
| 100 | 2330 | 440 / 460 | 5.5 | 10 |
| 400 | 2315 | 445 / 455 | 14.1 | 28 |
| 1000 | 2315 | 422 / 478 | 28.9 | 60 |

Unique patterns fall from 4330 to about 2300 by generation 80, then stay inside 2267–2352 for the rest of the run. The minimum is 2267 at generation 610. Strengthen and write stay near 430 and 470 after generation 100.

Mean broadcast strength is still rising at the end, by about 0.04 per generation over generations 800–1000. The last generations bounce between the high 20s and the mid 30s, which reads as a plateau around 30. The matched slots underneath are near strength 60 and still gaining.

Dominant-meme complexity is 0.238 at the start and 0.239 at generation 1000. The standing strings are still ordinary balanced bit patterns.

## What that steady state is

The early drop is duplicate formation. Agents start with almost private random strings (4330 distinct patterns in 4500 slots). A write copies a neighbor's broadcast, so one string begins to occupy more than one slot, and the evicted string is usually a one-off from the initial draw. By generation 100 each distinct string is stored about twice (4500 / 2300). Further writes mostly exchange one circulating string for another, and the unique count stops moving.

The writes never stop. A random neighbor is still outside every stored slot about half the time: the match radius is 4 bits out of 16, and the pool holds 5 strings. About 470 writes per generation replace a tenth of the grid's slots. The weakest slot is the one replaced, so a confirmed slot is spared, and the new string comes in at strength 1. Half the broadcasts measured each generation are those fresh writes. That pulls the reported mean down to 29 at generation 1000, while the slots that actually matched sit near strength 60.

Sixty confirmations in a thousand generations means the slot being restated has not been the winner all along. Hearings often land closer to some other slot, or they miss and a new string is written. An old confirmed string can sit in the pool without being the one sent.

The grid has thinned the initial noise into a cloud of lightly shared strings, and it keeps turning over about a tenth of its slots every generation. A particular string is not what an agent keeps saying.
