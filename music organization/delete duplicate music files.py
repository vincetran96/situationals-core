import re
from pathlib import Path
from typing import List, Set


ROOT = "./test_music_files"

# Get all file paths in the folder
root_path = Path(ROOT)
all_file_paths: List[Path] = [] # Type hint
for file_path in root_path.rglob("*"):
    if file_path.is_file():
        all_file_paths.append(file_path)

# For each file path, find its matches
# We're interested in the part before ".mp3" part of the file name
to_delete_file_paths: Set[Path] = set()
for target_path in all_file_paths:
    if target_path not in to_delete_file_paths:
        target_name = str(target_path).split(".mp3")[0]
        target_regex_pattern = re.compile(re.escape(target_name) + r" \d")
        for search_path in all_file_paths:
            search_name = str(search_path).split(".mp3")[0]
            if target_regex_pattern.match(search_name):
                print(f"Found duplicate: {search_name}")
                print(f"Of core name: {target_name}")
                to_delete_file_paths.add(search_path)
print("Here are the file paths to delete:")
print(to_delete_file_paths)

# Remove the duplicates
for file_path in to_delete_file_paths:
    file_path.unlink()
print("Found duplicates have been deleted")
