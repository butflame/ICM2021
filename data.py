import csv
import os
from pathlib import Path
from functools import lru_cache

BASE_DIR = Path(__file__).resolve().parent

data_by_artist_fp = os.path.join(BASE_DIR, 'raw_data', 'data_by_artist.csv')
full_music_data_fp = os.path.join(BASE_DIR, 'raw_data', 'full_music_data.csv')
influence_data_fp = os.path.join(BASE_DIR, 'raw_data', 'influence_data.csv')
artist_data_fp = os.path.join(BASE_DIR, 'raw_data', 'artist_data.csv')

with open(data_by_artist_fp) as f:
    data_by_artist = list(csv.DictReader(f))

with open(full_music_data_fp) as f:
    full_music_data = list(csv.DictReader(f))

with open(influence_data_fp) as f:
    influence_data = list(csv.DictReader(f))

with open(artist_data_fp) as f:
    artist_data = list(csv.DictReader(f))

genres = set([t["main_genre"] for t in artist_data])

# 所有相似程度分析将音乐特征feature_keys和音乐类型category_keys分开进行

music_feature_keys = (
    "danceability",
    "energy",
    "valence",
    "tempo",
    "loudness",
    # mode和key为离散型数据，在计算相似度时影响较大且意义较小，放弃
    # "mode",
    # "key",
)

music_category_keys = (
    "acousticness",
    "instrumentalness",
    "liveness",
    "speechiness",
    # "explicit",  同上，且98340首歌中，仅3647首该值为False，放弃
)

# 这一组大概不需要用到
music_desc_keys = (
    "duration_ms",
    "popularity",
    "year",
    "release_date",
    "song_title",
    "count",
)

artist_data_by_id = {
    d["artist_id"]: d
    for d in data_by_artist
}

artist_feature_data_by_id = {
    d["artist_id"]: {
        k: d[k]
        for k in music_feature_keys
    }
    for d in data_by_artist
}

artist_feature_values_by_id = {
    d["artist_id"]: [
        float(d[k])
        for k in music_feature_keys
    ]
    for d in data_by_artist
}
