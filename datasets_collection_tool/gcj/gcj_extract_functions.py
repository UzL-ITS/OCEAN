from pathlib import Path
import json
from tree_sitter import Language, Parser
from collections import namedtuple, defaultdict
import subprocess

Language.build_library(
    # Store the library in the `build` directory
    'build/my-languages.so',
    ["tree-sitter-cpp"]
)

CPP_LANGUAGE = Language('build/my-languages.so', 'cpp')

parser = Parser()
parser.set_language(CPP_LANGUAGE)

query = CPP_LANGUAGE.query(
    """
(function_declarator declarator: (identifier) @name) @definition.function
"""
)

Found_Function = namedtuple("Function", ["name", "start", "end"])

directory = "2022r3/solutions/"
all_files = [filename for filename in Path(directory).rglob("*.cpp")]
output_dir = "analyzed_files/2022r3/real_code/"
Path(output_dir).mkdir(parents=True, exist_ok=True)

def find_closing_bracket(file, brackets, line, index):
    count = None
    #print(line, index)
    while count is None or count > 0:
        index += 1
        if index == len(file[line]):
            line += 1
            index = 0
        if line >= len(file):
            return None
        if file[line][index] == brackets[0]:
            if not count:
                count = 1
            else:
                count += 1
        elif file[line][index] == brackets[1]:
            if count is None:
                return None
            count -= 1
    return line

def create_function_stats(repopath, filepath, found_functions):
    with open(f"{repopath}{filepath}") as fp:
        current_file = fp.readlines()
    file_list = []
    for function_name in found_functions:
        """start, end = find_function(current_file, function_name)
        if start is None or end is None:
            continue
        #authors = calculate_authors(file, start, end)"""
        #print(function_name)
        function_end = find_closing_bracket(current_file, "{}", function_name.end[0], function_name.end[1])
        if function_end is None:
            print(f"Function {function_name.name} in file {filepath} has no closing bracket", function_name.end)
            continue
        function_dict ={"name": function_name.name}
        function_dict["code"] = "".join(current_file[function_name.start[0]:function_end+1])
        function_dict["author"] = filepath.split("/")[-1].split(".")[:-2] 
        file_list.append(function_dict.copy())
    return file_list

for target_file in all_files:
    with open(target_file, "rb") as fp:
            code = fp.read()
    tree = parser.parse(code)
    root_node = tree.root_node
    captures = [node[0] for node in query.captures(root_node) if node[0].type == "identifier"]

    with open(target_file, "r") as file:
        lines = file.readlines()
    found_functions = [Found_Function(lines[c.start_point[0]][c.start_point[1]:c.end_point[1]], c.start_point, c.end_point) for c in captures]
    function_stats = create_function_stats(directory, "".join(str(file.name).split(directory, 1)[1:]), found_functions)
    if function_stats:
        with open(f"{output_dir}{str(file.name).split(directory, 1)[1]}.json", "w") as target_fp:
            json.dump(function_stats, target_fp)
    
