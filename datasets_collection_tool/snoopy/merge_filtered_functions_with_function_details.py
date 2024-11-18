import json

filtered_functions = "openssh_portable/filtered_functions_above_70.json"
function_detail_files = ["openssh_portable/function_details_scp.json", "openssh_portable/function_details_sftp-server.json", "openssh_portable/function_details_sftp.json", "openssh_portable/function_details_ssh-agent.json", "openssh_portable/function_details_ssh-keygen.json", "openssh_portable/function_details_ssh-keyscan.json", "openssh_portable/function_details_ssh.json", "openssh_portable/function_details_sshd.json"]
target_file = "openssh_portable/filtered_functions_above_70_with_details.json"

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