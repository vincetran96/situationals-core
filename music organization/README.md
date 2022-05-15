# What?
Scripts to organize your (Apple) music

# How to Use
## Deciding what script to use
### Scenarios
#### 1. Delete duplicate music files

Suppose you have a bunch of duplicate music files like so:
```
Hello.mp3
Hello 1.mp3
Hello 2.mp3
```
All these files are in the same folder. Then use `delete_duplicate_music_files.py`

#### 2. Move all music files in sub-directories to just one directory
Use `move_all_music_files_to_one_place.py`


#### 3. Download music from Deezer
Create an `.env` file in the envs like the `.example_env` file

Modify or create your input tracks to download like the `example_deezer_dl.json` file in the `download_inputs` folder

## Command
- Change the path names in the file you choose to run
- Simply run `python script_name.py`
