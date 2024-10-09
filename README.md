## source code of paper 《Shortcut2Secrets: A Path-based Differential Fault Attack》

### A complete DFA will include two files: xx_encryption.py and xx_filtering_key.py. xx is the concrete cipher.

*xx_encryption.py*: inject the fault and collect keystreams, generate the meerging path with MIP-GA

*xx_filtering_key.py*: filter the candidate key set according to the merging path

For Elisabeth-b4, we only generate the merging path and estimate the complexity theoretically.

### The function of other files:

*NLUT_and_LUT_generate.py*: genenerate the function h according to [HMS23]

*construct_diff_tables.py*: compute and store the filter table T for different h

*calculate_distribution.py*: count the distribution for all filter tables

