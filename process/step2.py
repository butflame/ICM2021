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
    artist_datas = [Artist(d) for d in data_by_artist]
    focus_points, groups = kmeans(
        artist_datas,
        k=20,  # genre数量
        eva_diff=Artist.diff,
        eva_avg=Artist.avg,
        threshold=0.05,  # fixme: 可以自己调整, 大一点可以跑快点，越小可以越精确
    )
    with open(os.path.join(BASE_DIR, 'process_data', 'step2_artist_kmeans.json'), 'w') as f:
        f.write(json.dumps({
            "focus_points": focus_points,
            "groups": groups,
        }))
    #
    # # full_music_datas
    # music_datas = [Artist(d) for d in full_music_data]
    # focus_points, groups = kmeans(
    #     music_datas,
    #     k=20,  # genre数量
    #     eva_diff=Artist.diff,
    #     eva_avg=Artist.avg,
    #     threshold=0.05,  # fixme: 可以自己调整
    # )
    # with open(os.path.join(BASE_DIR, 'process_data', 'step2_music_kmeans.json'), 'w') as f:
    #     f.write(json.dumps({
    #         "focus_points": focus_points,
    #         "groups": groups,
    #     }))


if __name__ == "__main__":
    run()
