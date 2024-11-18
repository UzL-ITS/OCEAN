import json
from collections import defaultdict

COUNT_FUNCTIONS_WO_AUTHOR = True

input_file = "all_authors_from_ast_without_tests.json"
target_file = "unique_functions_marked.json"

with open(input_file) as fp:
    all_files = json.load(fp)

function_names_count = defaultdict(int)
for file in all_files:
    for function in file["functions"]:
        if COUNT_FUNCTIONS_WO_AUTHOR or function["authors"]:
            function_names_count[function["name"]] += 1

unique_functions = []
for file in all_files:
    file_dict = {"file": file["file"], "functions": []}
    for function in file["functions"]:
        function_dict = function.copy()
        function_dict["unique"] = function_names_count[function["name"]] == 1
        file_dict["functions"].append(function_dict)
    unique_functions.append(file_dict)

with open(target_file, "w") as fp:
    json.dump(unique_functions, fp, indent=2)

