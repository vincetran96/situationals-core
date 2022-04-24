import shutil
from pathlib import Path
from typing import List


ORIGINAL_PATH = "./test_music_files/test_subdir0"
TARGET_PATH = "./test_music_files"

# Get all file paths in the folder
original_path = Path(ORIGINAL_PATH)
all_file_paths: List[Path] = []
for file_path in original_path.rglob("*"):
    if file_path.is_file():
        all_file_paths.append(file_path)

# Move each file to the target path
# Get base file name to overwrite move
target_path = Path(TARGET_PATH)
for file_path in all_file_paths:
    base_file_name = file_path.name
    print(f"Moving {base_file_name} to target path")
    shutil.move(file_path, target_path.joinpath(base_file_name))
 