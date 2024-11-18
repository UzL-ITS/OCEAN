import os

def grab_results(threshold=0):
    folders = os.listdir("results/analyzed_files")
    output_dir = "results/analysis_results"
    os.makedirs(output_dir, exist_ok=True)
    num_authors = 0
    num_functions = 0
    num_projects = 0
    for folder in folders:
        if not os.path.isdir(f"results/analyzed_files/{folder}") or not os.path.exists(f"results/analyzed_files/{folder}/num_authors_and_functions.txt"):
            continue
        with open(f"results/analyzed_files/{folder}/num_authors_and_functions.txt") as f:
            line = f.readline()
            num_authors += int(line.split(" ")[4])
            num_functions += int(line.split(" ")[1])
            num_projects += 1
        os.system(f"cp results/analyzed_files/{folder}/fixed_filtered_functions_above_{threshold}_with_details* results/analysis_results/{threshold}_fixed/")
    with open(f"results/analysis_results/{threshold}_fixed/num_authors_and_functions.txt", "w") as f:
        f.write(f"Total number of authors: {num_authors}\n")
        f.write(f"Total number of functions: {num_functions}\n")
    print(f"Total number of authors: {num_authors}")
    print(f"Total number of functions: {num_functions}")
    print(f"Total number of projects: {num_projects}")

if __name__ == "__main__":
    grab_results()

            
