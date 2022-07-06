'''Download tracks from Deezer using an input file
'''

import json
import argparse
import re
from pathlib import Path

import streamrip
from dotenv import dotenv_values
from thefuzz import fuzz


# Dotenv values
dotenvs = dotenv_values("envs/.env")
print(dotenvs)

# CLI args
parser = argparse.ArgumentParser(description="Download tracks from Deezer")
parser.add_argument(
    "tracks_json",
    help="Path to JSON file containing tracks to download; see example_deezer_dl.json"
)
parser.add_argument(
    "log_path",
    help="Path to where to contain the log file"
)
parser.add_argument(
    "--arl",
    help="Your Deezer ARL; not required if you have the ARL in the .env file"
)
args = parser.parse_args()
tracks_json_path_str = args.tracks_json
log_path_str = args.log_path
deezer_arl = args.arl or dotenvs['DEEZER_ARL']
if not deezer_arl:
    raise ValueError("Deezer ARL must be provided")

# Load original (OG) tracks from JSON
# The JSON contains keys as OG filename,
#   and OG token (title + artist)
tracks_json_path = Path(tracks_json_path_str)
tracks_json_path_parent = tracks_json_path.parent
with open(tracks_json_path_str, "r", encoding="utf-8") as tracks_jsonfile:
    og_tracks_dict = json.load(tracks_jsonfile)

# Deezer client
deezer_client = streamrip.clients.DeezerClient()
deezer_client.login(arl=deezer_arl)

# Logs
log_path = Path(log_path_str)

# Do a search for each track then download;
# Use a try-except block to prevent interruption
#   and log erroneous tracks to a file
# Only attempt to look into the first 5 results;
#   For each track, compare the deezer token (title + artist)
#   to its OG token to see how similar they are,
#   and the threshold is 70%,
#   then write the loggings to a file
MAX_SIMILARITY_SCORE = 0.7 * 100 + 0.3 * (100 + 100)
SIMILARITY_SCORE_THRESHOLD = 0.7
LOG_DELIMITER = "\t"
processed_filenames = []
for filename, og_token in og_tracks_dict.items():
    try:
        # Token must be sanitized so Deezer can search
        sanitized_og_token = re.sub(r'[^A-Za-z0-9 ]+', '', og_token)
        
        result = deezer_client.search(sanitized_og_token, media_type="track")
        dz_downloaded_tracks = []
        if result:
            dz_5_tracks = result['data'][:5]
            for dz_track_dict in dz_5_tracks:
                dz_token = dz_track_dict['title'] + " " + dz_track_dict['artist']['name']
                token_set_ratio = fuzz.token_set_ratio(sanitized_og_token, dz_token)
                token_sort_ratio = fuzz.token_sort_ratio(sanitized_og_token, dz_token)
                token_partial_ratio = fuzz.token_set_ratio(sanitized_og_token, dz_token)
                similarity_score = \
                    0.7 * token_set_ratio \
                    + 0.3 * (token_sort_ratio + token_partial_ratio)
                similarity_score_ratio = similarity_score / MAX_SIMILARITY_SCORE

                # Proceed to download the track if similarity score
                # meets threshold
                if similarity_score_ratio >= SIMILARITY_SCORE_THRESHOLD:
                    print(
                        f"Similarity score met threshold, downloading {dz_track_dict['title']} - {dz_track_dict['artist']['name']}"
                    )
                    top_result = streamrip.media.Track(
                        client=deezer_client,
                        id=dz_track_dict['id'],
                        part_of_tracklist=True
                    )
                    top_result.load_meta()
                    top_result.download(quality=1)
                    dz_downloaded_tracks.append(
                        dz_token + f" - ID: {dz_track_dict['id']}"
                    )
        with open(
            log_path.joinpath("deezer_downloads.txt"), "a", encoding="utf-8"
        ) as logfile:
            logfile.write(
                filename \
                + LOG_DELIMITER \
                + str(dz_downloaded_tracks) \
                + "\n"
            )
        processed_filenames.append(filename)
    except streamrip.exceptions.ItemExists:
        with open(
            log_path.joinpath("deezer_downloads.txt"), "a", encoding="utf-8"
        ) as logfile:
            logfile.write(
                filename \
                + LOG_DELIMITER \
                + str(dz_downloaded_tracks) \
                + "\n"
            )
        processed_filenames.append(filename)
    except Exception as exc:
        print(f"Exception on {filename}")
        print("Dumping remaining files to JSON words map")
        og_tracks_dict_remaining = {
            filename: og_token for filename, og_token in og_tracks_dict.items() \
                if filename not in processed_filenames
        }
        with open(
            tracks_json_path_parent.joinpath(
                "remaining.json"
            ),
            "w",
            encoding="utf-8"
        ) as remaining_file:
            json.dump(og_tracks_dict_remaining, remaining_file)
        raise exc
