# Generic-MITLP

This repository contains the implementation of multiple flavours of time-lock puzzles:
- Delegated Generic Multiple Instance Time-Lock Puzzle
- Generic Multiple Instance Time-Lock Puzzle
- [Multiple Instance Time-Lock Puzzle by Abadi & Kiayias](https://doi.org/10.1007/978-3-662-64331-0_28)
- [Original Time-Lock Puzzle by Rivest, Shamir & Wagner](https://dl.acm.org/doi/10.5555/888615)

## Installation
`pip install -r requirements.txt`

## Testing
Includes tests for all implemented puzzles. Run with

```sh
pytest
```

## Benchmarks
`benchmark_squarings.py` - Find how many squarings a CPU can do in 1 second

`benchmark_puzzles.py` - Find the run time of each algorithm for all puzzles

`benchmark_tlp_solve_single.py` - Find the run time of solving a single TLP; useful in making sure the benchmarking is correct

### Squaring Benchmark Results
| CPU                                                                  | Squarings per second |         |
|:---------------------------------------------------------------------|---------------------:|--------:|
|                                                                      |                 1024 |    2048 |
| Apple M1                                                             |              2260000 |  845000 |
| Intel Haswell @2.4MHz                                                |              1683087 |  671000 |
| Azure B1ls_v1 running Intel(R) Xeon(R) Platinum 8272CL CPU @ 2.60GHz |              1400000 | |
