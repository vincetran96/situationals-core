'''Download tracks from Deezer using an input file
'''

import json
import argparse
import streamrip
from dotenv import dotenv_values


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
    "--arl",
    help="Your Deezer ARL; not required if you have the ARL in the .env file"
)
args = parser.parse_args()
tracks_json_path = args.tracks_json
deezer_arl = args.arl or dotenvs['DEEZER_ARL']

# Load tracks list from JSON
with open(tracks_json_path, "r", encoding="utf-8") as tracks_jsonfile:
    tracks_dict = json.load(tracks_jsonfile)

# Deezer client
deezer_client = streamrip.clients.DeezerClient()
deezer_client.login(arl=deezer_arl)

# Do a search for each track then download
for track in tracks_dict['tracks']:
    result = deezer_client.search(track, media_type="track")
    top_result = streamrip.media.Track(
        client=deezer_client,
        id=result['data'][0]['id'],
        part_of_tracklist=True
    )
    top_result.load_meta()

    print(f"Downloading {top_result}")
    top_result.download(quality=1)
