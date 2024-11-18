import os
import subprocess
import yaml
from pathlib import Path
from all_function_authors_from_ast import all_function_authors_from_ast
from mark_duplicate_functions import mark_duplicate_functions
from filter_below_threshold import filter_below_threshold
from merge_filtered_functions_with_function_details import merge_filtered_functions_with_function_details

NUM_PACKAGES = None

def full_conan_analysis():
    default_dir = "/src"
    os.chdir(default_dir)
    all_recipes = os.listdir("conan-center-index/recipes")
    progress_counter = 0
    success_counter = 0
    for recipe_folder in all_recipes:
        if NUM_PACKAGES is not None and progress_counter >= NUM_PACKAGES:
            break
        os.chdir(default_dir)
        progress_counter += 1
        if progress_counter % 20 == 0:
            print(f"\nRemoving last 20 packages from conan cache\n")
            p = subprocess.Popen(f"conan remove \"*\" -c", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=f"{default_dir}", text=True)
            out, err = p.communicate()
            if p.returncode != 0:
                print(f"Error removing packages from conan cache: {err}")
        print(f"\nAnalyzing {recipe_folder} ({progress_counter}/{len(all_recipes)})")
        try:

            # Load recipe to find the GitHub URL
            with open(f"conan-center-index/recipes/{recipe_folder}/all/conandata.yml") as f:
                target_yaml = yaml.safe_load(f)["sources"]
            target_version = list(target_yaml)[0]
            print(f"Target version: {target_version}")
            github_url = None
            if isinstance(target_yaml[target_version]["url"], str):
                url = target_yaml[target_version]["url"]
                if "github.com" in url:
                    print(f"GitHub URL: {url}")
                    github_url = url
            else:
                for url in target_yaml[target_version]["url"]:
                    if "github.com" in url:
                        print(f"GitHub URL: {url}")
                        github_url = url
                        break
            if github_url is None:
                print("No GitHub URL found")
                continue

            # Clone the repo
            clone_url = "/".join(github_url.split("/")[:5]) + ".git"
            clone_name = github_url.split("/")[4]
            clone_tag = github_url.split("/")[-1].replace(".tar.gz", "").replace(".zip", "").replace(".tgz", "").replace("tar.bz2", "")
            if os.path.exists(f"{default_dir}/analysis/{clone_name}"):
                print(f"{recipe_folder} is already cloned!")
            else:
                p = subprocess.Popen(f"git clone {clone_url}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=f"{default_dir}/analysis/")
                out, err = p.communicate()
                if p.returncode != 0:
                    print(f"Error cloning {recipe_folder}: {err.decode()}")
                    continue
                os.chdir(f"analysis/{clone_name}")
                p = subprocess.Popen(f"git checkout {clone_tag}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=f"{default_dir}/analysis/{clone_name}")
                out, err = p.communicate()
                if p.returncode != 0:
                    print(f"Error checking out {recipe_folder} with tag {clone_tag}: {err.decode()}, trying to checkout with different name...")
                    clone_tag = github_url.split('/')[-2]
                    p = subprocess.Popen(f"git checkout {clone_tag}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=f"{default_dir}/analysis/{clone_name}")
                    out, err = p.communicate()
                    if p.returncode != 0:
                        print(f"Error checking out {recipe_folder} with tag {clone_tag}: {err.decode()}, no solution found")
                        continue
                
                print(f"Cloned {clone_url} at tag {clone_tag}")

            # build the recipe
            p = subprocess.Popen(f"conan create --version=\"{target_version}\" --build=\"*\" -vnotice -tf=\"\" --options=shared=True .", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=f"{default_dir}/conan-center-index/recipes/{recipe_folder}/all", text=True)
            out, err = p.communicate()
            if p.returncode != 0:
                p = subprocess.Popen(f"conan create --version=\"{target_version}\" --build=\"*\" -vnotice -tf=\"\" .", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=f"{default_dir}/conan-center-index/recipes/{recipe_folder}/all", text=True)
                out, err = p.communicate()
                if p.returncode != 0:
                    print(f"Error building {recipe_folder}: {err}")
                    continue
            try:
                bin_path = err.split(f"{recipe_folder}/{target_version}: Package folder ")[1].split("\n")[0]
                if os.path.exists(f"{bin_path}/bin"):
                    bin_path += "/bin/"
                elif os.path.exists(f"{bin_path}/lib"):
                    bin_path += "/lib/"
                else:
                    print(f"Error finding bin path for {recipe_folder}")
                    continue
            except:
                print(f"Error finding bin path in conan output for {recipe_folder}")
                continue
            print(f"Bin path: {bin_path}")

            # analyze with Ghidra
            os.makedirs("/src/analysis/ghidra_projects", exist_ok=True)
            p = subprocess.Popen(f"/src/ghidra_11.0.3_PUBLIC/support/analyzeHeadless /src/analysis/ghidra_projects {clone_name} -import {bin_path} -processor x86:LE:64:default -cspec gcc -noanalysis", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            if p.returncode != 0:
                print(f"Error analyzing {recipe_folder} (trying to continue...): {err.decode()} {out.decode()}")
            p = subprocess.Popen(f"/src/ghidra_11.0.3_PUBLIC/support/analyzeHeadless /src/analysis/ghidra_projects {clone_name} -recursive -process -postScript extract_various_formats.py", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            if p.returncode != 0:
                print(f"Error analyzing {recipe_folder}: {err.decode()} {out.decode()}")
                continue
            print(f"Ghidra analysis complete for {recipe_folder}")

            # run analysis from ast
            os.chdir(f"{default_dir}/analysis/analyzed_files/{clone_name}")
            function_analysis_file = f"/src/analysis/{clone_name}/all_authors_from_ast_wo_tests_with_code_{clone_name}.json"
            function_analysis_folder = f"/src/analysis/analyzed_files/{clone_name}/"
            function_detail_files = [str(filename) for filename in Path(function_analysis_folder).rglob(f"*.json")]
            all_function_authors_from_ast(f"{default_dir}/analysis/{clone_name}/", function_detail_files, function_analysis_file) 

            duplicated_marked_file = f"{function_analysis_folder}unique_functions_marked.json"
            mark_duplicate_functions(function_analysis_file, duplicated_marked_file)

            stat_file = f"{function_analysis_folder}num_authors_and_functions.txt"
            threshold = 0.7
            filtered_file = f"{function_analysis_folder}filtered_functions_above_{threshold}.json"
            num_authors = filter_below_threshold(duplicated_marked_file, filtered_file, stat_file, threshold)
            if num_authors == 0:
                print(f"No authors found for {recipe_folder}")
                continue

            merged_function_details_file = f"{function_analysis_folder}filtered_functions_above_{threshold}_with_details_{clone_name}.json"
            merge_filtered_functions_with_function_details(filtered_file, function_detail_files, merged_function_details_file)

            success_counter += 1
            print(f"Analysis complete for {recipe_folder} ({success_counter}/{progress_counter})")

            
        except Exception as e:
            print(f"Error analyzing {recipe_folder}: {e}")
            continue


if __name__ == "__main__":
    full_conan_analysis()