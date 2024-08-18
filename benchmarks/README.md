
## Benchmarks
`benchmark_squarings.py` - Find how many squarings a CPU can do in 1 second; output for a range of CPUs is in [benchmarks/results.md](./results.md).

`benchmark_puzzles.py` - Find the run time of each algorithm for all puzzles; output will be in `benchmarks/out/benchmark<timestamp>.csv`.

`benchmark_size.py` - Find the size of the output of each puzzle algorithm

`benchmark_tlp_solve_single.py` - Find the run time of solving a single TLP; useful in making sure the benchmarking is correct

Run with:
```bash
sudo python3 benchmarks/benchmark_<type>.py
```
