# 分风格计算各年度的popularity
import json
from data import full_music_data, artist_data_by_id
import csv


def run():
    to_use = list(filter(lambda x: len(json.loads(x["artists_id"])) == 1, full_music_data))  # length: 93930
    for t in to_use:
        t["artist_id"] = str(json.loads(t.pop("artists_id"))[0])
        t["genre"] = artist_data_by_id[t["artist_id"]]["main_genre"]
    keys = sorted(list(to_use[0].keys()))
    group_by_genre = {}
    for t in to_use:
        group_by_genre.setdefault(t["genre"], {}).setdefault(t["year"], []).append(t)
    # 每个流派的年度数据
    # for genre in group_by_genre:
    #     with open(f"{genre.replace('/', '')}_by_year.csv", "w") as f:
    #         w = csv.DictWriter(f, keys)
    #         w.writeheader()
    #         for y in group_by_genre[genre]:
    #             w.writerows(group_by_genre[genre][y])

    # 每个流派的年度popularity平均值数据
    avg_popularity_by_genre_and_year = {}
    years = set()

    for genre in group_by_genre:
        for y in group_by_genre[genre]:
            years.add(y)
            popularities = [float(t["popularity"]) for t in group_by_genre[genre][y]]
            avg_popularity_by_genre_and_year.setdefault(genre, {})[y] = round(sum(popularities) / len(popularities), 1)

    years = sorted(list(years))
    with open("../process_data/q5/q5_avg_popularity_by_genre_and_year.csv", 'w') as f:
        w = csv.DictWriter(f, ["genre", *years])
        w.writeheader()
        for genre in avg_popularity_by_genre_and_year:
            tmp = {"genre": genre}
            for y in avg_popularity_by_genre_and_year[genre]:
                tmp[y] = avg_popularity_by_genre_and_year[genre][y]
            w.writerow(tmp)


if __name__ == "__main__":
    run()
