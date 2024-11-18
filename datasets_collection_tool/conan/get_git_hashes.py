import os
import json
import subprocess

def get_git_hashes():
    target_files = os.listdir("results/analysis_results/0")
    for target_file in target_files:
        if target_file.endswith(".json"):
            target_folder = target_file.split("filtered_functions_above_0_with_details_")[1].split(".json")[0]
            p = subprocess.Popen(f"git rev-parse HEAD", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=f"results/{target_folder}", text=True)
            out, err = p.communicate()
            if p.returncode != 0:
                print(f"Could not get hash for {target_folder}: {err}")
                continue
            hash = out.strip()
            with open(f"results/analysis_results/0/{target_file}") as f:
                data = json.load(f)
            output_data = {"commit_hash": hash, "data": data}
            os.makedirs("results/analysis_results/with_hash", exist_ok=True)
            with open(f"results/analysis_results/with_hash/{target_file}", "w") as f:
                json.dump(output_data, f)

if __name__ == "__main__":
    get_git_hashes()