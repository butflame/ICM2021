import matplotlib.pyplot as plt
import networkx as nx

from algos.cosine_similarity import cosine_similarity
from data import *


def make_nodes_and_edge():
    nodes = set()
    edges = set()
    for d in influence_data:
        if d["influencer_main_genre"] != d["follower_main_genre"]:
            continue
        influencer = d["influencer_id"]
        follower = d["follower_id"]
        # influencer = "_".join([d["influencer_id"], d["influencer_main_genre"]])
        # follower = "_".join([d["follower_id"], d["follower_main_genre"]])
        nodes.add(influencer)
        nodes.add(follower)
        edges.add((influencer, follower))

    to_remove = set()
    for e in edges:
        reversed_influence = (e[1], e[0])
        if reversed_influence in edges:
            to_remove.add(e)
            to_remove.add(reversed_influence)
    edges -= to_remove

    #
    # with open(os.path.join(BASE_DIR, "process_data", "influece_nodes_and_edges.txt"), 'w') as f:
    #     f.write(
    #         "\n".join(nodes)
    #     )
    #     f.write(
    #         "\n".join(edges)
    #     )
    #
    to_draw = sorted(list(edges))[-100:]
    # make_directed_graph(to_draw)  # fixme

    make_influence_paths_of_influence(edges)


def make_directed_graph(edges):
    plt.figure(1, (24, 24))
    G = nx.DiGraph()
    for e in edges:
        G.add_edge(e[0], e[1])

    pos = nx.spring_layout(G)  # positions for all nodes

    # nodes
    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=50,
    )

    # edges
    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=edges,
        width=1,
        edge_color="gray",
        style="dashed",
        min_source_margin=15,
        min_target_margin=15,
    )

    # labels
    nx.draw_networkx_labels(
        G,
        pos,
        font_size=12,
    )
    plt.show()


# 用于描述影响和追随关系的辅助类
class Artist:
    def __init__(self, id_):
        self.id = id_
        self.followers = set()
        self.influencers = set()

    @property
    def is_original(self):
        return not self.influencers

    def incluence(self, other):
        self.followers.add(other)

    def follow(self, other):
        self.influencers.add(other)

    def __repr__(self):
        return f"<Artist {self.id}>"


def make_influence_paths_of_influence(edges):
    artists = {}
    for e in edges:
        influencer_id, follower_id = e[0], e[1]
        if str(influencer_id) not in artist_data_by_id or str(follower_id) not in artist_data_by_id:
            continue
        artists.setdefault(influencer_id, Artist(influencer_id)).incluence(
            artists.setdefault(follower_id, Artist(follower_id))
        )
        artists.setdefault(follower_id, Artist(follower_id)).follow(
            artists.setdefault(influencer_id, Artist(influencer_id))
        )

    # 没有被人影响的artists
    originals = list(filter(lambda x: x.is_original, artists.values()))
    # 选取追随者最多的5个歌手进行分析
    picked_originals = sorted(originals, key=lambda x: -len(x.followers))[:5]

    paths = []
    stack = [[o] for o in picked_originals]
    while stack:
        if len(paths) >= 100000:  # 最多选十万条。。着不住了
            break
        cur = stack.pop()
        tail = cur[-1]
        if not tail.followers:
            # 只选长度5以上的影响链
            if len(cur) >= 10:
                paths.append(cur)
        else:
            for f in list(tail.followers)[:10]:  # 最多选10个追随者，不然数据量太大了
                if f not in cur:  # 这里是为了切断循环影响
                    stack.append([*cur, f])

    artists_ids_in_path = [
        [str(a.id) for a in p]
        for p in paths
    ]
    artists_names_in_path = [
        [artist_data_by_id[str(a.id)]["artist_name"] for a in p]
        for p in paths
    ]
    features_by_paths = [
        [artist_feature_values_by_id[str(a.id)] for a in p]
        for p in paths
    ]
    cosine_similarity_by_path = [
        [cosine_similarity(p[i], p[i - 1]) for i in range(1, len(p))]
        for p in features_by_paths
    ]
    with open(os.path.join(BASE_DIR, 'process_data', 'q5_artists_ids_in_path.csv'), 'w') as f:
        f.write("\n".join([",".join(path) for path in artists_ids_in_path]))
    with open(os.path.join(BASE_DIR, 'process_data', 'q5_artists_names_in_path.csv'), 'w') as f:
        f.write("\n".join([",".join(path) for path in artists_names_in_path]))
    with open(os.path.join(BASE_DIR, 'process_data', 'q5_cosine_similarity_by_path.csv'), 'w') as f:
        f.write("\n".join([",".join([str(t) for t in path]) for path in cosine_similarity_by_path]))

    return


def __find_path(start_node: Artist):
    if not start_node.followers:
        return [[start_node.id]]

    ret = []
    for follower in start_node.followers:
        for p in __find_path(follower):
            ret.append([start_node.id, *p])
    return ret


if __name__ == "__main__":
    make_nodes_and_edge()
