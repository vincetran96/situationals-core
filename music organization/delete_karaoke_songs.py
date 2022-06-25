'''Delete karaoke songs
'''

from pathlib import Path
from typing import Set


MUSIC_PATH = Path(r"E:\music")

# Search for Karaoke
to_delete_file_paths: Set[Path] = set()
for file_path in MUSIC_PATH.rglob("*.mp3"):
    if file_path.is_file():
        base_name = file_path.name.lower()
        if base_name.find("tribute") > -1:
            to_delete_file_paths.add(file_path)
            print(f"Found {base_name}")

# Remove
for file_path in to_delete_file_paths:
    file_path.unlink()
    print(f"Deleted {file_path}")
