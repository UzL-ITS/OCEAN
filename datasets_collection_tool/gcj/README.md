The files in this directory can be used to create a dataset containing binary and higher level representations of code written in the Google Code Jam. The original datasets were retrieved from [GitHub](https://github.com/Jur1cek/gcj-dataset).

1. Use `transform_csv_to_c.py` to create C and C++ files containing the code from the csv.
2. Use `compile_submissions.sh` to compile all created code samples using g++ with debug-symbols and O0
3. Use `gcj_extract_functions.py` to extract all functions from the code that can be found via ASTs
4. Use `merge_analyzed_files.py` to merge the various code representations retrieved from Ghidra (see instructions of parent directory) with the analysis retrieved from step 3.