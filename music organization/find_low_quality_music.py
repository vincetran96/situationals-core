'''Find songs with low bitrates and move them into a folder
'''

import argparse
import shutil
import re
import json
import logging
from pathlib import Path
from eyed3 import mp3


def sanitize_title_artist(title_artist: str):
    '''Sanitizes title artist string
    to improve the neutrality of the track name
    '''
    forbidden_words = [
        "extended mix",
        "extended version",
        "radio edit",
        "extended edit",
        "original mix"
    ]
    for word in forbidden_words:
        title_artist = title_artist.replace(word, "")

    return title_artist

# Logging
logging.basicConfig(level=logging.ERROR)

parser = argparse.ArgumentParser(description="Find low-quality music")
parser.add_argument(
    "music_path",
    help="Path to all music"
)
parser.add_argument(
    "bitrate",
    type=int,
    default=128,
    help="Bitrate threshold for low quality music (in KBPS)"
)
parser.add_argument(
    "--lq_folder",
    action=argparse.BooleanOptionalAction,
    default=False,
    help="Whether to move all low quality files to a folder"
)
args = parser.parse_args()
music_path_str = args.music_path
low_quality_bit_rate = args.bitrate
is_lq_folder = args.lq_folder
print(f"Scanning for low-quality music files in {music_path_str}")
print(f"Low quality bitrate set to {low_quality_bit_rate} KBPS")

# Music path and make low quality path
music_path = Path(music_path_str)
low_quality_path = music_path.joinpath("low_quality")
low_quality_path.mkdir(parents=True, exist_ok=True)

# Mapping of filename to words in its filename;
#   The keys for these maps are the actual filenames
#   because they're the only identifiers of them for
#   me in Windows
all_music_words_map = {}
low_quality_words_map = {}
words_regex = re.compile(r"(\w[\w']*\w|\w)")
words_map_path = music_path.joinpath("words_map")
words_map_path.mkdir(parents=True, exist_ok=True)

# Bitrate regular expression
bit_rate_regex = r"[0-9]+"

# For each music file in the music path,
# get its core name (w/o extension),
# map that core name to list of words in it,
# read the MP3 info, extract the bitrate using regex,
# move the file to a low quality folder if bitrate <= threshold
for music_file in music_path.rglob("*.mp3"):
    base_file_name = music_file.name
    core_file_name = music_file.stem
    file_words = words_regex.findall(core_file_name.lower())

    # Find low quality, make mapping, and move
    # The default title of the mp3 file are from file_words;
    # If there is a title tag, use that instead
    mp3_file = mp3.Mp3AudioFile(music_file)
    bit_rate = int(re.search(bit_rate_regex, mp3_file.info.bit_rate_str).group(0))
    mp3_tags = mp3_file.tag
    mp3_title = " ".join(file_words)
    if mp3_tags.title:
        mp3_title = mp3_tags.title.lower()
    mp3_artist = ""
    if mp3_tags.artist:
        mp3_artist = mp3_tags.artist.lower()

    # Construct a unified string of title + artist
    #   to be used in Deezer download later;
    # It has to be sanitized of forbidden words
    #   so that Deezer can find them
    title_artist = mp3_title + " " + mp3_artist
    sanitized_title_artist = sanitize_title_artist(title_artist)
    all_music_words_map[core_file_name] = sanitized_title_artist

    if bit_rate <= low_quality_bit_rate:
        # low_quality_words_map[core_file_name] = file_words
        low_quality_words_map[core_file_name] = sanitized_title_artist
        print(
            f"File {base_file_name} is low-quality; It is: {sanitized_title_artist}"
        )
        if is_lq_folder:
            print(f"Moving it to {low_quality_path}")
            shutil.move(music_file, low_quality_path.joinpath(base_file_name))

# Write words map to JSON
print("Dumping words map to JSON")
with open(
    words_map_path.joinpath("all_music.json"), "w", encoding="utf-8") as all_words_file:
    json.dump(all_music_words_map, all_words_file)
with open(
    words_map_path.joinpath("low_quality.json"), "w", encoding="utf-8") as lq_words_file:
    json.dump(low_quality_words_map, lq_words_file)
