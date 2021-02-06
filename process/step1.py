# 选择歌曲数最多的20个歌手，以data_by_artist中的风格数据和类型数据作为基准，对每个歌手的所有歌曲进行相似度分析，以验证使用余弦相似度的可行性
import csv
import json
import os

from algos.cosine_similarity import cosine_similarity
from data import data_by_artist, full_music_data, music_feature_keys, music_category_keys, BASE_DIR


def pick_three_artist_with_most_music():
    # 选出歌曲数最多的20个歌手
    picked_artists = sorted(data_by_artist, key=lambda x: x["count"], reverse=True)[:20]
    picked_artist_ids = [int(a["artist_id"]) for a in picked_artists]

    # 使用data_by_artist中的歌手数据作为基准
    picked_artist_base_feature_params = {}
    for pick_artist in picked_artists:
        picked_artist_base_feature_params[int(pick_artist["artist_id"])] = [
            float(pick_artist[k])
            for k in music_feature_keys
        ]
    picked_artist_base_category_params = {}
    for pick_artist in picked_artists:
        picked_artist_base_category_params[int(pick_artist["artist_id"])] = [
            float(pick_artist[k])
            for k in music_category_keys
        ]

    # 找到3个歌手的所有歌曲
    musics_by_artist = {}
    for music in full_music_data:
        artists_id = json.loads(music["artists_id"])
        for aid in artists_id:
            if aid in picked_artist_ids:
                musics_by_artist.setdefault(aid, []).append(music)

    # 对每个歌手，计算所有歌曲特征和类型的余弦相似性，取平均值
    feature_similarity_by_artist = {}
    category_similarity_by_artist = {}

    for aid, musics in musics_by_artist.items():
        for music in musics:
            music_feature_params = [
                float(music[k])
                for k in music_feature_keys
            ]
            music_category_params = [
                float(music[k])
                for k in music_category_keys
            ]
            feature_similarity_by_artist.setdefault(aid, []).append(
                cosine_similarity(
                    picked_artist_base_feature_params[aid],
                    music_feature_params,
                )
            )
            category_similarity_by_artist.setdefault(aid, []).append(
                cosine_similarity(
                    picked_artist_base_category_params[aid],
                    music_category_params,
                )
            )

    feature_similarity_by_artist = {
        k: round(sum(v) / len(v), 5)
        for k, v in feature_similarity_by_artist.items()
    }
    category_similarity_by_artist = {
        k: round(sum(v) / len(v), 5)
        for k, v in category_similarity_by_artist.items()
    }

    with open(os.path.join(BASE_DIR, 'process_data', 'step1_similarity_by_artist.csv'), 'w') as f:
        headers = ['artist_id', 'avg_feature_similarity', 'avg_category_similarity']
        writer = csv.DictWriter(f, headers)
        writer.writeheader()
        for aid in picked_artist_ids:
            row = {
                "artist_id": str(aid),
                "avg_feature_similarity": feature_similarity_by_artist[aid],
                "avg_category_similarity": category_similarity_by_artist[aid],
            }
            writer.writerow(row)


if __name__ == "__main__":
    pick_three_artist_with_most_music()
