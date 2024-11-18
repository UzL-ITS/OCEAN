This docker downloads the entire conan database, builds all projects that are available on conan and hosted on Github, and then runs our pipeline including Ghidra and the analysis scripts.

To run this pipeline:
1. Build the Docker out of this directory
2. Start the Docker with the command `docker run -ti --mount type=bind,source=<dir on host device>,target=/src/analysis <name of build>`
    -   Because conan is a big project, you should ideally mount an external directory on the host
3. Inside the running Docker, run `python3 full_conan_analysis.py`
4. All results will be stored in the folder `/src/analysis/analyzed_files/`
5. On the host machine, you can collect all results by running the script `grab_results.py` or using `grab_results_with_threshold.py` if the stats files created by the docker are not available anymore

`get_git_hashes.py` can be used to add commit hashes of the GitHub repositories to the data retrieved by `grab_results.py`

All other files in this directory and the `scripts` directory are used inside the docker to setup conan (`conan_profile`), configure Ghidra (`extract_various_formats.py`) and map functions to authors (`scripts` directory)