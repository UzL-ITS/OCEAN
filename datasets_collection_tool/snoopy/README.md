# Setup
- The project contains a `Dockerfile` that can be used to get an environment in which 'Git-author' is already installed. After building it can be run with `docker run -ti <Name of Image>`.

- Alternatively you can build the project locally as well. To setup the project, you need to clone and build git from https://github.com/mxz297/Git-author and add it to your path. The installation requires Openssl 1.0.2 as well as python2, all higher versions do not work for building.
Additionally you will need to install the python-package `treesitter` in Python3.

# Files
To create a dataset from a GitHub repository follow these steps after cloning:

1. `all_function_authors_from_ast.py` searches a directory for all of its .c files and scans every file for function names given in the json resulting of the Ghidra analysis (see parent directory for Ghidra instructions). Afterwards, it outputs all corresponding authors for the found functions into `all_authors_from_ast*.json`

2. `mark_duplicate_functions.py` adds a `unique` tag to every function in a json and outputs it into `unique_functions_marked.json`. If you set `COUNT_FUNCTIONS_WO_AUTHOR` to false, functions that share their name with a function that has no attributed authors still count as unique.

3. `filter_below_threshold.py` creates json files in which all functions have the `unique` tag set and the main author of the function has contributed more than `THRESHOLD` to this function.

4. `merge_filtered_functions_with_function_details.py` creates a combined json file from filter_below_threshold and the file with all code representations from Ghidra.

## Other useful scripts

- `stat_plots.py` displays some plots to evaluate the findings of `all_function_authors_from_ast.py`
- `functions_from_ast.py` searches through a given directory and outputs all functions found through creation of ASTs with tree-sitter and outputs them into `ast_functions*.json`