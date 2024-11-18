from pathlib import Path
import json
import random

merge_dir = "analyzed_files/2022r3/"
code_dir = merge_dir + "real_code/"
detail_dir = merge_dir + "function_details/"
target_dir = merge_dir + "all_info/"

Path(target_dir).mkdir(parents=True, exist_ok=True)
all_files = [filename for filename in Path(code_dir).rglob("*.json")]

merged_files = {}

for file in all_files:
    with open(file) as f:
        code = json.load(f)
    try:
        with open(detail_dir + f"function_details_{file.name.replace(code_dir, '', 1).replace('.cpp', '')}") as f:
            details = json.load(f)
    except FileNotFoundError: # file could not be compiled and is therefore missing
        continue

    function_names = {}
    for function in code:
        function_names[function["name"]] = function_names.get(function["name"], 0) + 1
    
    to_be_removed = []
    for function in code:
        for detail in details:
            if function["name"] == detail["name"] and function_names[function["name"]] > 1:
                random_number = random.randint(1, 1000)
                function["name"] += f"_{random_number}"
                detail["name"] += f"_{random_number}"
                
            if function["name"] == detail["name"]:
                function["raw"] = detail["raw"]
                function["p_code"] = detail["p_code"]
                function["c_code"] = detail["c_code"]
                function["assembly"] = detail["assembly"]
                break
        else:
            to_be_removed.append(function)
    
    for function in to_be_removed:
        code.remove(function)
    with open(target_dir + file.name.replace(code_dir, '', 1), "w") as f:
        json.dump(code, f, indent=4)
    merged_files[file.name.replace(code_dir, '', 1).strip(".json")] = code

with open(target_dir + "_all_info_from_competition.json", "w") as f:
    json.dump(merged_files, f, indent=4)
