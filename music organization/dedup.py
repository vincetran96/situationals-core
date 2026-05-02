import json


IN_NAME = "AppleMusic-Playlist-All.json"


with open(IN_NAME, "r") as infile:
    in_json = json.load(infile)

data = in_json[0]
tracks = data["tracks"]

data_copy = {
    "snapshotId": data["snapshotId"],
    "description": data["description"],
    "service": data["service"],
    "name": f"{data['name']} - Dedup",
    "serviceId": data["serviceId"]
}

# Dedup using track ID
track_map = {}
for track in tracks:
    if track["isrc"] in track_map:
        continue
    track_map[track["isrc"]] = track

data_copy["tracks"] = list(track_map.values())
out_json = [data_copy]

print(len(data_copy["tracks"]))

filename = IN_NAME.split(".json")[0]
with open(f"out/{filename}-Dedup.json", "w", encoding="utf-8") as outfile:
    json.dump(out_json, outfile, ensure_ascii=False)
