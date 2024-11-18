import json

def filter_below_threshold(input_file="php/unique_functions_marked.json", target_file=f"php/filtered_functions_above_70.json", stat_file=None, threshold=0.7):

    with open(input_file) as fp:
        all_files = json.load(fp)

    selected_functions = []
    for file in all_files:
        file_dict = {"file": file["file"], "functions": []}
        for function in file["functions"]:
            if function["unique"] and function["authors"] and function["authors"][function["leading_author"]] >= threshold:
                file_dict["functions"].append(function.copy())
        if file_dict["functions"]:
            selected_functions.append(file_dict)

    all_authors = set()
    num_functions = 0
    for file in selected_functions:
        for function in file["functions"]:
            num_functions += 1
            all_authors.add(function["leading_author"])

    print(f"Selected {num_functions} functions from {len(all_authors)} authors")
    if stat_file:
        with open(stat_file, "w") as fp:
            fp.write(f"Selected {num_functions} functions from {len(all_authors)} authors\n")
            

    with open(target_file, "w") as fp:
        json.dump(selected_functions, fp, indent=2)

    return len(all_authors)

