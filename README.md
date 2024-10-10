## source code of paper 《Shortcut2Secrets: A Path-based Differential Fault Attack》

### A complete DFA will include two files: xx_encryption.py and xx_filtering_key.py. xx is the concrete cipher.

*xx_encryption.py*: inject the fault and collect keystreams, generate the meerging path with MIP-GA.

*xx_filtering_key.py*: filter the candidate key set according to the merging path.

For Elisabeth-b4, we only generate the merging path and estimate the complexity theoretically.

### The function of other files:

*NLUT_and_LUT_generate.py*: genenerate the function h according to [HMS23].

*construct_diff_tables.py*: compute and store the filter table T for different h. Due to the size limit of files in Github, we only upload the T of Elisabeth-4 here as an example. For the filter tables of Elisabeth-b4 and Margrethe-18-4, readers can generate them with this file.

*calculate_distribution.py*: count the distribution for all filter tables.

### The function of folders:

E4_Diff_tables: store the filter table T for Elisabeth-4.

distribution: store the calculated distribution for all filter tables.

tmp_result_file: store the keystream information and temporary files.

useful_result: store the useful merging paths.

