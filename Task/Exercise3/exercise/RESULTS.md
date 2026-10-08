# Results: where the training time went

## 1. Baseline

| Measure | Value |
| --- | --- |
| Time per step (ms) | |
| Test accuracy (%) | |

## 2. The agent's guess, before any profile

| Rank | What the agent expected to dominate | Its estimated share of the time |
| --- | --- | --- |
| 1 | | |
| 2 | | |
| 3 | | |

Did it follow the `TODO` comment? 

## 3. Baseline profile: five most expensive operations

**GPU table** (sorted by GPU time)

| Operation | GPU time | Share of total | Calls |
| --- | --- | --- | --- |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |

**CPU table** (sorted by CPU time)

| Operation | CPU time | Share of total | Calls |
| --- | --- | --- | --- |
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |

Roughly how much of each step is the GPU actually busy? 

## 4. Fixes, one at a time

| # | Change | Agent's predicted time per step (ms) | Measured time per step (ms) | Speedup vs baseline | Test accuracy (%) |
| --- | --- | --- | --- | --- | --- |
| 0 | Baseline | — | | 1.0× | |
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

## 5. What dominated the time

Write a short paragraph: what dominated the time, how you knew, and whether the `TODO` was right.
Point at the numbers in the tables above.
