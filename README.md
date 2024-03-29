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
