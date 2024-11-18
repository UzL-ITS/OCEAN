from pathlib import Path
import json
from tree_sitter import Language, Parser
from collections import namedtuple, defaultdict
import subprocess

directory = "php-src/"
function_name_files = ["function_details_php.json"]
target_file = "all_authors_from_ast_wo_tests_with_code_php.json"
use_cpp = False

Language.build_library(
    # Store the library in the `build` directory
    'build/my-languages.so',
    ["tree-sitter-c", "tree-sitter-cpp"]
)

C_LANGUAGE = Language('build/my-languages.so', 'c')
CPP_LANGUAGE = Language('build/my-languages.so', 'cpp')

parser = Parser()

if use_cpp:
    parser.set_language(CPP_LANGUAGE)
    query = CPP_LANGUAGE.query("""(function_declarator declarator: (identifier) @name) @definition.function""")
else:
    parser.set_language(C_LANGUAGE)
    query = C_LANGUAGE.query("""(function_declarator declarator: (identifier) @name) @definition.function""")

# define a named tuple to store the function name as well as its start and end point
Found_Function = namedtuple("Function", ["name", "start", "end"])

file_ending = "cpp" if use_cpp else "c"
all_files = [filename for filename in Path(directory).rglob(f"*.{file_ending}")]
files_without_tests = [filename for filename in all_files if "test" not in str(filename) and '/doc/' not in str(filename) and '/demos/' not in str(filename) and '/checks/' not in str(filename) and '/3rdparty/' not in str(filename) and '/samples/' not in str(filename)]
print(f"Found {len(all_files)} files")
print(f"Found {len(files_without_tests)} files without tests")

function_names = []
for function_name_file in function_name_files:
    with open(function_name_file) as fp:
        function_names = json.load(fp)
    function_names.extend([function_name["name"].strip() for function_name in function_names])

def get_git_author_statistics(repopath, filepath):
    lines = subprocess.run(["git-author", "-W", filepath], cwd=repopath, text=True, capture_output=True).stdout.split("\n")
    line_statistics = []
    line_stat = []
    while lines:
        line = lines.pop(0)
        if not line:
            line_statistics.append(line_stat.copy())
            line_stat.clear()
        else:
            if ":" in line:
                continue
            line_stat.append(line.strip())
    return line_statistics

def calculate_authors(line_statistics, start_line, end_line):
    authors = defaultdict(float)
    for line_number in range(start_line, end_line+1):
        if line_number >= len(line_statistics):
            #print(line_number, len(line_statistics))
            continue
        for line in line_statistics[line_number]:
            line = line.split(" ")
            authors[" ".join(line[1:-1]).strip()] += float(line[-1].split("/")[0])
    #divide score of all authors by total score
    total_score = sum(authors.values())
    for author in authors:
        authors[author] /= total_score
    return authors.copy(), total_score

def calculate_leading_author(line_statistics, start_line, end_line):
    authors, total_score = calculate_authors(line_statistics, start_line, end_line)
    if authors:
        return authors, max(authors, key=authors.get), total_score
    else:
        return authors, "Author not found", total_score

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
    line_statistics = get_git_author_statistics(repopath, filepath)
    #print(filepath)
    with open(f"{repopath}{filepath}") as fp:
        current_file = fp.readlines()
    leading_authors = {"file": repopath + filepath, "functions": []}
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
        function_dict["authors"], function_dict["leading_author"], function_dict["total_score"] = calculate_leading_author(line_statistics, function_name.start[0], function_end)
        leading_authors["functions"].append(function_dict.copy())
    return leading_authors

with open(target_file, "w") as target_fp:
    target_fp.write("[")
    for file in files_without_tests:
        with open(file, "rb") as fp:
            code = fp.read()
        tree = parser.parse(code)
        root_node = tree.root_node
        captures = [node[0] for node in query.captures(root_node) if node[0].type == "identifier"]
        try:
            with open(file, "r") as file:
                lines = file.readlines()
        except:
            continue
        found_functions = [Found_Function(lines[c.start_point[0]][c.start_point[1]:c.end_point[1]], c.start_point, c.end_point) for c in captures if lines[c.start_point[0]][c.start_point[1]:c.end_point[1]] in function_names]
        function_stats = create_function_stats(directory, "".join(str(file.name).split(directory, 1)[1:]), found_functions)
        if function_stats["functions"]:
            json.dump(function_stats, target_fp)
            target_fp.write(",\n")
    target_fp.seek(target_fp.tell() - 2, 0)
    target_fp.write("]")
                
