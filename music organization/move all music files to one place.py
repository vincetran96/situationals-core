import os
import shutil

ORIGINAL_PATH = "/Path/To/Music/Files"
TARGET_PATH = "/New/Path/To/Music/Files"

# Get all file paths in the folder
all_file_paths = []
for path, subdirs, files in os.walk(ORIGINAL_PATH):
    for name in files:
        all_file_paths.append(os.path.join(path, name))

# Move each file to the target path
# Get base file name to overwrite move
for file_path in all_file_paths:
    base_file_name = os.path.basename(file_path)
    print(f"Moving {base_file_name} to target path")
    shutil.move(file_path, os.path.join(TARGET_PATH, base_file_name))
