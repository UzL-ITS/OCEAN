# Overview
This directory includes all steps needed to create the various datasets that are presented and used in the OCEAN paper.
All datasets contain functionwise author information including main author and distribution of authors in function and various formats like raw binary, assembly and decompiled code.
- `conan/` includes a docker that can be used out of the box to fetch all repositories contained in the Conan package manager and create a dataset from them
- `gcj/` includes scripts that can be used to create a dataset based on a csv containing code of various authors and samples
- `snoopy/` includes scripts that can be used to create a dataset from any GitHub repository containing C/C++ code.

# Ghidra
All three directories use [Ghidra](https://ghidra-sre.org/) to analyze a binary file and create various representations. Our approach has been tested with Ghidra 11.0.1, but should work with other versions as well. Ghidra can be used in headless mode with `extract_various_formats.py` as post-script. 

- `extract_various_formats.py` can be put into `<path to Ghidra>/Ghidra/Features/Python/ghidra_scripts/extract_various_formats.py` so that Ghidra detects the file automatically by name

1. `<path to Ghidra>/support/analyzeHeadless <path to Ghidra projects dir> <Project name> -import <target files or directory> -noanalysis`
2. `<path to Ghidra>/support/analyzeHeadless <path to Ghidra projects dir> <Project name> -process -postScript extract_various_formats.py`