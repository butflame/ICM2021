import random

def kmeans(datas, k, evaluation, initiation=None, threshold=0.01):
    """
    kmeans算法实现
    :param datas: 数据集
    :param k: k值
    :param evaluation: 对数据项距离计算的方法
    :param initiation: 初始聚类点
    :param threshold: 判断是否停止循环的 整体距离优化率阈值
    :return:
    """
    assert isinstance(datas, (list, tuple))
    dimension = None
    for item in datas:
        assert isinstance(item, (list, tuple))
        if not dimension:
            dimension = len(item)
        assert dimension
        assert len(item) == dimension
    assert isinstance(k, int)
    assert callable(evaluation)
    if initiation is not None:
        assert isinstance(initiation, (list, tuple))
        assert len(initiation) == dimension
    assert isinstance(threshold, float)
    assert 0 < threshold < 1

    # 初始化聚类点
    if not initiation:
        initiation = []
        while len(initiation) < k:
            choice = random.choices(datas, k)
            if choice not in initiation:
                initiation.append(choice)

    # 开始聚类
    total_diff = 2 ** 16  # 用一个足够大的数作为整体距离初始值
    while 1:
        data_sets = [[] for i in range(k)]  # 被聚类的原数据点
        # data可能需要用类来做，因为需要标识



