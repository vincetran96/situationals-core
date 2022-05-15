'''Find if we already have a similar file name for 
a low-quality music file
'''

import json
import difflib
import argparse
import logging
from pathlib import Path


def get_max_matching_block(matching_blocks: list):
    '''Gets the matching block with the greatest size
    from a list of matching blocks;

    If the matching block has length of 1, return None
    '''
    if len(matching_blocks) == 1:
        return None
    sorted_blocks = sorted(matching_blocks, key=lambda x: x[2], reverse=True)
    
    return sorted_blocks[0]

# Logging
logging.basicConfig(level=logging.ERROR)

parser = argparse.ArgumentParser(description="Find low-quality file name in all music")
parser.add_argument(
    "music_path",
    help="Path to all music"
)
parser.add_argument(
    "--low_quality_sub_path",
    default="low_quality",
    help="Sub-path to LQ music"
)
parser.add_argument(
    "--words_map_sub_path",
    default="words_map",
    help="Sub-path to words map"
)

args = parser.parse_args()
music_path_str = args.music_path
lq_subpath_str = args.low_quality_sub_path
wordsmap_subpath_str = args.words_map_sub_path

music_path = Path(music_path_str)
lq_path = music_path.joinpath(lq_subpath_str)
wordsmap_path = music_path.joinpath(wordsmap_subpath_str)

with open(
    wordsmap_path.joinpath("all_music.json"), "r", encoding="utf-8") as all_words_file:
    all_music_words_map = json.load(all_words_file)
with open(
    wordsmap_path.joinpath("low_quality.json"), "r", encoding="utf-8") as lq_words_file:
    low_quality_words_map = json.load(lq_words_file)

master_match = {}
for lq_core_name, lq_words in low_quality_words_map.items():
    top_matching_blocks = []
    for all_core_name, all_words in all_music_words_map.items():
        if all_core_name != lq_core_name:
            matching_blocks = difflib.SequenceMatcher(
                None, lq_words, all_words).get_matching_blocks()
            max_mb = get_max_matching_block(matching_blocks)
            if max_mb:
                top_matching_blocks.append([all_core_name, max_mb])
    if top_matching_blocks:
        top_matching_blocks = sorted(
            top_matching_blocks, key=lambda x: x[1][2], reverse=True)
        master_match[lq_core_name] = top_matching_blocks[0]
        print(f"{lq_core_name}: {master_match[lq_core_name]}")

print(master_match)
with open(
    wordsmap_path.joinpath("master_match.json"), "w", encoding="utf-8") as mastermatch_file:
    json.dump(master_match, mastermatch_file)
