import json

THRESHOLD = 0.7

input_file = "unique_functions_marked.json"
target_file = f"filtered_functions_above_{int(THRESHOLD*100)}.json"

with open(input_file) as fp:
    all_files = json.load(fp)

selected_functions = []
for file in all_files:
    file_dict = {"file": file["file"], "functions": []}
    for function in file["functions"]:
        if function["unique"] and function["authors"] and function["authors"][function["leading_author"]] >= THRESHOLD:
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
        

with open(target_file, "w") as fp:
    json.dump(selected_functions, fp, indent=2)

