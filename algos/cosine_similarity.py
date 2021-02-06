# 定义: https://baike.baidu.com/item/%E4%BD%99%E5%BC%A6%E7%9B%B8%E4%BC%BC%E5%BA%A6/17509249?fr=aladdin
import math


def cosine_similarity(a, b):
    assert isinstance(a, (list, tuple)) and isinstance(
        b, (list, tuple)
    ), "only list or tuple is acceptable"
    assert len(a) == len(
        b
    ), "the two params of cosine_similarity must have equal length"

    ret = sum([a[i] * b[i] for i in range(len(a))]) / (
            math.sqrt(sum(t ** 2 for t in a)) * math.sqrt(sum(t ** 2 for t in b))
    )
    return round(ret, 4)
