from tree_sitter import Language, Parser
from pprint import pprint
from pathlib import Path
import json

Language.build_library(
    # Store the library in the `build` directory
    'build/my-languages.so',
    ["tree-sitter-c"]
)

C_LANGUAGE = Language('build/my-languages.so', 'c')

parser = Parser()
parser.set_language(C_LANGUAGE)

query = C_LANGUAGE.query(
    """
(function_declarator declarator: (identifier) @name) @definition.function
"""
)

directory = "openssl/"
all_files = [filename for filename in Path(directory).rglob("*.c")]
files_without_tests = [filename for filename in all_files if "test" not in str(filename) and '/doc/' not in str(filename) and '/demos/' not in str(filename)]
output_file = "ast_functions_without_tests.json"

with open(output_file, "w") as output_fp:
    output_fp.write("[")
    for target_file in files_without_tests:
        with open(target_file, "rb") as file:
            code = file.read()

        tree = parser.parse(code)
        root_node = tree.root_node

        captures = [node[0] for node in query.captures(root_node) if node[0].type == "identifier"]

        with open(target_file, "r") as file:
            lines = file.readlines()
            function_names = [lines[c.start_point[0]][c.start_point[1]:c.end_point[1]] for c in captures]

        json.dump({"file": str(target_file), "functions": function_names}, output_fp)
        output_fp.write(",\n")
    output_fp.seek(output_fp.tell() - 2, 0)
    output_fp.write("]")
