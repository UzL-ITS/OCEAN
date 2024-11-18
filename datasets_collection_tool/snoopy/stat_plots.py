import matplotlib.pyplot as plt
import json
from collections import defaultdict
from pprint import pprint

input_file = "openssl/all_authors_from_ast_without_tests.json"

with open(input_file) as fp:
    all_files = json.load(fp)

authors_per_function = defaultdict(int)

for file in all_files:
    for function in file["functions"]:
        authors_per_function[len(function["authors"])] += 1

authors_per_function = dict(sorted(authors_per_function.items(), key=lambda item: item[0]))

main_author_contrib_per_function = defaultdict(int)

for file in all_files:
    for function in file["functions"]:
        if function["authors"]:
            main_author_contrib_per_function[round(max([float(v) for v in function["authors"].values()]), 1)] += 1

main_author_contrib_per_function = dict(sorted(main_author_contrib_per_function.items(), key=lambda item: item[0]))

all_main_author_contrib = sum(main_author_contrib_per_function.values())
min_main_author_contrib = {}
for x in main_author_contrib_per_function.keys():
    min_main_author_contrib[x] = sum([v for k, v in main_author_contrib_per_function.items() if k <= x]) / all_main_author_contrib

max_main_author_contrib = {}
for x in main_author_contrib_per_function.keys():
    max_main_author_contrib[x] = sum([v for k, v in main_author_contrib_per_function.items() if k >= x]) / all_main_author_contrib

function_names_count = defaultdict(int)
for file in all_files:
    for function in file["functions"]:
        function_names_count[function["name"]] += 1

undistinguished_functions = defaultdict(int)
for item in function_names_count.items():
    undistinguished_functions[item[1]] += 1

undistinguished_functions = dict(sorted(undistinguished_functions.items(), key=lambda item: item[0]))
    
            
fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(1, 5, figsize=(25, 5))

ax1.bar(authors_per_function.keys(), authors_per_function.values())
ax1.set_xlabel("Number of authors")
ax1.set_ylabel("Number of functions")
ax1.set_title("Number of authors per function")

ax2.plot(main_author_contrib_per_function.keys(), main_author_contrib_per_function.values())
ax2.set_xlabel("Main author contribution")
ax2.set_ylabel("Number of functions")
ax2.set_title("Main author contribution per function")

ax3.plot(min_main_author_contrib.keys(), min_main_author_contrib.values())
ax3.set_xlabel("Main author contribution")
ax3.set_ylabel("Number of functions")
ax3.set_title("Main author contribution per function (cumulative)")

ax4.plot(max_main_author_contrib.keys(), max_main_author_contrib.values())
ax4.set_xlabel("Main author contribution")
ax4.set_ylabel("Number of functions")
ax4.set_title("Main author contribution per function (cumulative)")

ax5.bar(undistinguished_functions.keys(), undistinguished_functions.values())
ax5.set_xlabel("Number of functions with the same name")
ax5.set_ylabel("Number of functions")
ax5.set_title("Number of functions with the same name")

pprint(undistinguished_functions)


plt.tight_layout()
plt.show()

