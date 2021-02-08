# 分风格计算各年度的popularity
import csv
import json

from data import full_music_data, artist_data_by_id, flat_music_data


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

    obviously_popularity_increase_rate_by_genre = {}
    for genre in avg_popularity_by_genre_and_year:
        increase_rate_by_year = []
        for i in range(len(years) - 1):
            prev = avg_popularity_by_genre_and_year[genre].get(years[i])
            next_ = avg_popularity_by_genre_and_year[genre].get(years[i + 1])
            if not prev or not next_:
                rate = 0
            else:
                rate = round((float(next_) - float(prev)) * 100 / float(prev), 2)
            if rate > 100:  # 增幅达50%认为是变革式的流行
                increase_rate_by_year.append((years[i + 1], rate))
        obviously_popularity_increase_rate_by_genre[genre] = increase_rate_by_year

    with open("../process_data/q5/obviously_popularity_increase_rate_by_genre.csv", 'w') as f:
        w = csv.DictWriter(f, ["genre", *years])
        w.writeheader()
        for genre in obviously_popularity_increase_rate_by_genre:
            tmp = {"genre": genre}
            for year, rate in obviously_popularity_increase_rate_by_genre[genre]:
                tmp[year] = str(rate)
            w.writerow(tmp)

    # 在实现了变革式流行的年份发布了歌曲的歌手
    greatest_artist_with_genre_and_years = []
    for genre in obviously_popularity_increase_rate_by_genre:
        tmp = {
            "genre": genre
        }
        for year, _ in obviously_popularity_increase_rate_by_genre[genre]:
            tmp[year] = greater_artist_by_genre_and_year(genre, year)
        greatest_artist_with_genre_and_years.append(tmp)
    with open("../process_data/q5/greatest_artist_with_genre_and_years.csv", 'w') as f:
        w = csv.DictWriter(f, ["genre", *years])
        w.writeheader()
        w.writerows(greatest_artist_with_genre_and_years)

    return


def artists_with_avg_popularity_by_genre_and_year(genre, year):
    popularities_by_artist = {}
    for m in filter(lambda x: x["genre"] == genre and x["year"] == year, flat_music_data):
        popularities_by_artist.setdefault(m["artist_id"], []).append(float(m["popularity"]))
    return [(artist_data_by_id[k]["artist_name"], round(avg(v), 2)) for k, v in popularities_by_artist.items()]


def greater_artist_by_genre_and_year(genre, year):
    artists_with_pop = artists_with_avg_popularity_by_genre_and_year(genre, year)
    artists_with_pop.sort(key=lambda x: -x[1])
    return artists_with_pop[0][0]


def avg(iter):
    return sum(iter) / len(iter)


if __name__ == "__main__":
    run()
