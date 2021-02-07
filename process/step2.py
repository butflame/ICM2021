import csv
import json
import os

from algos.cosine_similarity import cosine_similarity
from algos.kmeans import kmeans
from data import music_feature_keys, data_by_artist, BASE_DIR, full_music_data


class Artist(dict):
    identity_keys = (
        "id", "name", "main_genre",
    )
    feature_keys = music_feature_keys

    @classmethod
    def diff(cls, a, b) -> float:
        feature_params_a = [float(a[k]) for k in cls.feature_keys]
        feature_params_b = [float(b[k]) for k in cls.feature_keys]
        return 1 - cosine_similarity(feature_params_a, feature_params_b)

    @classmethod
    def avg(cls, datas):
        for d in datas:
            assert isinstance(d, cls)

        ret = cls()
        for k in cls.feature_keys:
            all_params = [float(d[k]) for d in datas]
            ret[k] = sum(all_params) / len(all_params)
        return ret


def run():
    genre_by_artist = {}
    genres = set()
    artist_datas = []
    for d in data_by_artist:
        genre_by_artist[int(d["artist_id"])] = d["main_genre"]
        genres.add(d["main_genre"])
        artist_datas.append(Artist(d))

    focus_points, groups = kmeans(
        artist_datas,
        k=20,  # genre数量, 除开Unknown共19个
        eva_diff=Artist.diff,
        eva_avg=Artist.avg,
        threshold=0.01,
    )
    with open(os.path.join(BASE_DIR, 'process_data', 'step2_by_artist_focus_point.csv'), 'w') as f:
        writer = csv.DictWriter(f, music_feature_keys)
        writer.writeheader()
        writer.writerows(focus_points)

    genre_count_by_group = []
    for index, grouped_datas in enumerate(groups, start=1):
        tmp = {"group": str(index)}
        for d in grouped_datas:
            cur_genre = genre_by_artist.get(int(d['artist_id']), 'Unknown')
            tmp[cur_genre] = tmp[cur_genre] + 1 if cur_genre in tmp else 1
            for g in genres:
                tmp.setdefault(g, 0)
        genre_count_by_group.append(tmp)

    with open(os.path.join(BASE_DIR, 'process_data', 'step2_by_artist_genre_count_by_group.csv'), 'w') as f:
        # 每个聚类组中各个流派的分布
        header = ["group", *sorted(genres)]
        writer = csv.DictWriter(f, header)
        writer.writeheader()
        writer.writerows(genre_count_by_group)

    # full_music_datas
    music_datas = [Artist(d) for d in full_music_data]
    focus_points, groups = kmeans(
        music_datas,
        k=20,  # genre数量
        eva_diff=Artist.diff,
        eva_avg=Artist.avg,
        threshold=0.01,
    )
    with open(os.path.join(BASE_DIR, 'process_data', 'step2_by_music_focus_point.csv'), 'w') as f:
        writer = csv.DictWriter(f, music_feature_keys)
        writer.writeheader()
        writer.writerows(focus_points)

    genre_count_by_group = []
    for index, grouped_datas in enumerate(groups, start=1):
        tmp = {"group": str(index)}
        for d in grouped_datas:
            for artist_id in json.loads(d["artists_id"]):
                cur_genre = genre_by_artist[artist_id]
                tmp[cur_genre] = tmp[cur_genre] + 1 if cur_genre in tmp else 1
            for g in genres:
                tmp.setdefault(g, 0)
        genre_count_by_group.append(tmp)
    with open(os.path.join(BASE_DIR, 'process_data', 'step2_by_music_genre_count_by_group.csv'), 'w') as f:
        # 每个聚类组中各个流派的分布
        header = ["group", *sorted(genres)]
        writer = csv.DictWriter(f, header)
        writer.writeheader()
        writer.writerows(genre_count_by_group)


if __name__ == "__main__":
    run()
