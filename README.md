# Generic-MITLP

This repository contains the implementation of multiple flavours of time-lock puzzles:
- [Delegated Generic Multiple Instance Time-Lock Puzzle](./static/e_Print__of___D_Time_lock_puzzle.pdf)
- [Generic Multiple Instance Time-Lock Puzzle](./static/e_Print__of___D_Time_lock_puzzle.pdf)
- [Multiple Instance Time-Lock Puzzle by Abadi & Kiayias](https://doi.org/10.1007/978-3-662-64331-0_28)
- [Original Time-Lock Puzzle by Rivest, Shamir & Wagner](https://dl.acm.org/doi/10.5555/888615)

## Installation

Create virtual env:
```sh
 python3 -m venv .venv         
```

Activate virtual env:
```sh
source .venv/bin/activate
```

### Using pip-tools

Install pip-tools:
```sh
pip install pip-tools
```

Run pip-sync:
```sh
pip-sync
```

### Alternatively, you can install requirements manually.

Install requirements:
```sh   
pip install -r requirements.txt
```

Install dev requirements:
```sh
pip install -r requirements-dev.txt
```

## Development
Install editable package:
```sh
pip install -e .
```


Project uses `pip-tools` to manage dependencies.
Dependencies are listed in `pyproject.toml` under `[project]` -> `dependencies` and `[project.optional-dependencies]` -> `dev`.
To update dependencies, change pyproject.toml and run the `pip-compile` commands listed in the requirements files.

## Testing
Includes tests for all implemented puzzles. Run with

```sh
pytest
```

## Benchmarks
`benchmark_squarings.py` - Find how many squarings a CPU can do in 1 second

`benchmark_puzzles.py` - Find the run time of each algorithm for all puzzles

`benchmark_tlp_solve_single.py` - Find the run time of solving a single TLP; useful in making sure the benchmarking is correct
