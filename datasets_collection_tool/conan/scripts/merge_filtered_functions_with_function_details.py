import json

def merge_filtered_functions_with_function_details(filtered_functions = "php/filtered_functions_above_70.json", 
                                                   function_detail_files = ["php/function_details_php.json"], 
                                                   target_file = "php/filtered_functions_above_70_with_details_php.json"):

    with open(filtered_functions) as fp:
        filtered_functions_list = json.load(fp)

    function_detail_dict = {}
    for function_detail_file in function_detail_files:
        with open(function_detail_file) as fp:
            function_details = json.load(fp)
        for function_detail in function_details:
            function_detail_dict[function_detail["name"]] = function_detail

    new_filtered_functions_list = []
    for file in filtered_functions_list:
        new_filtered_functions_list.append(file.copy())
        new_filtered_functions_list[-1]["functions"] = []
        for function in file["functions"]:
            function = {**function_detail_dict[function["name"]], **function}
            new_filtered_functions_list[-1]["functions"].append(function)
        
    with open(target_file, "w") as fp:
        json.dump(new_filtered_functions_list, fp, indent=2)