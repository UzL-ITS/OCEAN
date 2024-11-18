import os
from pathlib import Path
from scripts.filter_below_threshold import filter_below_threshold
from scripts.merge_filtered_functions_with_function_details import merge_filtered_functions_with_function_details
from grab_results import grab_results

def grab_results_with_threshold(threshold=0):
    folders = os.listdir("results/analyzed_files")
    output_dir = f"results/analysis_results/{threshold}"
    os.makedirs(output_dir, exist_ok=True)
    for folder in folders:
        function_analysis_folder = f"results/analyzed_files/{folder}/"
        if not os.path.isdir(function_analysis_folder) or not os.path.exists(f"{function_analysis_folder}/unique_functions_marked.json"):
            continue
        duplicated_marked_file = f"{function_analysis_folder}unique_functions_marked.json"

        stat_file = f"{function_analysis_folder}num_authors_and_functions_{threshold}.txt"
        filtered_file = f"{function_analysis_folder}filtered_functions_above_{threshold}.json"
        num_authors = filter_below_threshold(duplicated_marked_file, filtered_file, stat_file, threshold)
        if num_authors == 0:
            continue
        merged_function_details_file = f"{function_analysis_folder}filtered_functions_above_{threshold}_with_details_{folder}.json"
        function_detail_files = [str(filename) for filename in Path(function_analysis_folder).glob(f"function_details_*.json")]
        merge_filtered_functions_with_function_details(filtered_file, function_detail_files, merged_function_details_file)
    grab_results(threshold)

if __name__ == "__main__":
    grab_results_with_threshold()
