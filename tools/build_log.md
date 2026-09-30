# tools/build_log.md — index build history

Appended automatically, one line per `python3 tools/sblgraph.py build`.
Format: `<timestamp>  rev=<git rev> files=N nodes=N edges=N <seconds> <KB>  dangling=N`

## Builds

Early entries record the debugging that fixed the first build. They are kept
deliberately: four defects were found and corrected during verification, and
these numbers are the evidence.

| # | build | files | nodes | edges | size | dangling | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | pre-fix | 557 | 1489 | 1081 | 1712 KB | 478 | graph walked gitignored `research/` corpora + scratch |
| 2 | scope fix | 34 | 358 | 471 | 612 KB | 82 | graph now follows git's view of the repo |
| 3-5 | intermed. | 34 | 358 | 471 | 612-616 KB | 82 | health/URL/orphan fixes; no graph-shape change |
| 6 | URL fix | 34 | 290 | 401 | 564 KB | 12 | URLs no longer resolved as repo paths |
| 7 | FTS fix | 34 | 290 | 401 | 932 KB | 12 | `body` column added; full-text index rebuilt |

Final state: **290 nodes, 401 edges, 932 KB, 12 dangling references, 0.09 s build.**

## Raw append log

- 2026-10-01 03:59:47  rev=72824c8 files=557 nodes=1489 edges=1081 0.33s 1712KB  dangling=478
- 2026-10-01 04:00:31  rev=c032cb1 files=34 nodes=358 edges=471 0.09s 612KB  dangling=82
- 2026-10-01 04:00:56  rev=c032cb1 files=34 nodes=358 edges=471 0.09s 616KB  dangling=82
- 2026-10-01 04:01:09  rev=c032cb1 files=34 nodes=358 edges=471 0.09s 612KB  dangling=82
- 2026-10-01 04:01:35  rev=c032cb1 files=34 nodes=290 edges=401 0.10s 564KB  dangling=12
- 2026-10-01 04:01:59  rev=c032cb1 files=34 nodes=290 edges=401 0.10s 932KB  dangling=12
- 2026-10-01 04:02:02  rev=c032cb1 files=34 nodes=290 edges=401 0.09s 932KB  dangling=12
- 2026-10-01 04:02:02  rev=c032cb1 files=34 nodes=290 edges=401 0.09s 932KB  dangling=12
- 2026-10-01 04:03:56  rev=c032cb1 files=36 nodes=334 edges=451 0.10s 1044KB  dangling=12
- 2026-10-01 04:04:40  rev=9dd372f files=37 nodes=351 edges=472 0.09s 1092KB  dangling=12
- 2026-10-01 04:05:08  rev=5b6ee7e files=37 nodes=351 edges=472 0.10s 1092KB  dangling=12
