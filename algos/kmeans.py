import random


def kmeans(datas, k, eva_diff, eva_avg, initiation=None, threshold=0.01):
    """
    kmeans算法实现
    :param datas: 数据集
    :param k: k值
    :param eva_diff: 对数据项距离计算的方法
    :param initiation: 初始聚类点
    :param threshold: 判断是否停止循环的 整体距离优化率阈值
    :return:
    """
    assert isinstance(datas, (list, tuple))
    # dimension = None
    # for item in datas:
    #     assert isinstance(item, (list, tuple))
    #     if not dimension:
    #         dimension = len(item)
    #     assert dimension
    #     assert len(item) == dimension
    assert isinstance(k, int)
    assert callable(eva_diff)
    assert callable(eva_avg)
    # if initiation is not None:
    #     assert isinstance(initiation, (list, tuple))
    #     assert len(initiation) == dimension
    assert isinstance(threshold, float)
    assert 0 < threshold < 1

    # 初始化聚类点
    if not initiation:
        initiation = []
        while len(initiation) < k:
            choice = random.choice(datas)
            if choice not in initiation:
                initiation.append(choice)

    # 开始聚类
    total_diff = 2 ** 16  # 用一个足够大的数作为整体距离初始值
    while 1:
        current_total_diff = 0
        grouped_data_sets = [[] for i in range(k)]  # 被聚类的原数据点
        # data可能需要用类来做，因为需要标识
        for data in datas:
            # 找到距离最近的原数据点
            min_diff, min_index = None, None
            for index, ini_data in enumerate(initiation):
                diff = eva_diff(data, ini_data)
                if min_diff is None:
                    min_diff, min_index = diff, index
                else:
                    if diff < min_diff:
                        min_diff, min_index = diff, index

            grouped_data_sets[min_index].append(data)
            current_total_diff += min_diff

        opt_rate = (total_diff - current_total_diff) / total_diff
        print(f"optimize total_diff {round(opt_rate * 100, 2)} percent from {total_diff} to {current_total_diff}")
        if abs(opt_rate) <= threshold:
            return initiation, grouped_data_sets
        else:
            for i in range(k):
                initiation[i] = eva_avg(grouped_data_sets[i])
            total_diff = current_total_diff
            # 继续下一轮
