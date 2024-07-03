### Squaring Benchmark Results]
https://learn.microsoft.com/en-us/azure/virtual-machines/vm-naming-conventions
- default - Intel x86-64 / p - ARM64 / a - AMD x86-64 
- l - low memory
- s - secure storage (not used)

| Machine                                  | CPU                                            | Squarings... | ...per second | Cost per hour |
|:-----------------------------------------|:-----------------------------------------------|-------------:|--------------:|--------------:|
|                                          |                                                |         1024 |          2048 |               |
| Apple MacBook Pro                        | Apple M1 Pro @ 3.23GHz                         |      2260000 |        845000 |           N/A |
| Dell Latitude 5421                       | 11th Gen Intel(R) Core(TM) i7-11850H @ 2.50GHz |      2025000 |        749000 |           N/A |
| University High Performance Cluster      | Intel Haswell @ 2.4GHz                         |      1683000 |        671000 |           N/A | 
| Azure B1ls_v1 (burst general computing)  | Intel(R) Xeon(R) Platinum 8272CL @ 2.60GHz     |      1399000 |        545000 |       US$0.01 |
| Azure B2ls_v2 (burst general computing)  | Intel(R) Xeon(R) Platinum 8370C @ 2.80GHz      |      1508000 |        573000 |       US$0.05 |
| Azure B2als_v2 (burst general computing) | AMD EPYC 7763 @2.45GHz                         |      1913000 |        685000 |       US$0.04 |
| Azure B2pls_v2 (burst general computing) | Ampere(R) Altra(R) @3.0GHz                     |       823000 |               |       US$0.04 |
| Azure F2s_v2 (compute optimized)         | Intel(R) Xeon(R) Platinum 8272CL @ 2.60GHz     |      1612000 |        628000 |       US$0.10 |
| Azure DS2_v2 (compute optimized)         | Intel(R) Xeon(R) E5-2673 v3 @ 2.40GHz          |      1201000 |        480000 |       US$0.14 |
| Azure D2as_v5 (compute optimized)        | AMD EPYC 7763 @ 2.45GHz                        |      1935000 |        686000 |       US$0.10 |
| Azure D2ls_v5 (compute optimized)        | Intel(R) Xeon(R) Platinum 8370C @ 2.80GHz      |      1509000 |        573000 |       US$0.10 |
| Azure D2pls_v5 (compute optimized)       | Ampere(R) Altra(R) @3.0GHz                     |       824000 |        262000 |       US$0.09 |
| Azure FX4mds (compute optimized)         | Intel(R) Xeon(R) Gold 6246R CPU @ 3.40GHz      |      1911000 |        736000 |       US$0.37 |