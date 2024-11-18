import json
from collections import defaultdict

def mark_duplicate_functions(input_file = "php/all_authors_from_ast_wo_tests_with_code_php.json", target_file = "php/unique_functions_marked.json", count_functions_wo_author = True):

    with open(input_file) as fp:
        all_files = json.load(fp)

    function_names_count = defaultdict(int)
    for file in all_files:
        for function in file["functions"]:
            if count_functions_wo_author or function["authors"]:
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

