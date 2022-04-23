import os
import re

ROOT = "/Path/To/Music/Files"

# Get all file paths in the folder
all_file_paths = []
for path, subdirs, files in os.walk(ROOT):
    for name in files:
        all_file_paths.append(os.path.join(path, name))

# For each file path, find its matches
# We're interested in the part before ".mp3" part of the file name
to_delete_file_paths = set()
for target_path in all_file_paths:
    if target_path not in to_delete_file_paths:
        target_name = target_path.split(".mp3")[0]
        target_regex_pattern = re.compile(re.escape(target_name) + r" \d")
        for search_path in all_file_paths:
            search_name = search_path.split(".mp3")[0]
            if target_regex_pattern.match(search_name):
                print(f"Found duplicate: {search_name}")
                print(f"Of core name: {target_name}")
                to_delete_file_paths.add(search_path)
print("Here are the file paths to delete:")
print(to_delete_file_paths)

# Remove the duplicates
for file_path in to_delete_file_paths:
    os.remove(file_path)
print("Found duplicates have been deleted")
