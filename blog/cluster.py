# -*- coding:utf8 -*-
# !/usr/bin/env python3

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from matplotlib import pyplot as plt
from collections import defaultdict
from functools import reduce
import numpy as np
import json
import random
from blog.models import JsonPost



def sort_cluster(n_samples, centers, labels, n_cluster):
    '''
    sort cluster by center distances
    :param n_samples: list, samples
    :param centers: list, cluster center
    :param labels: list, cluster result
    :param n_cluster: int, cluster num
    :return: list, sorted cluster [[sample_idx,..],..]
    '''
    frequency = [0] * n_cluster
    for i in labels:
        frequency[i] += 1
    # label: frequency

    # select the biggest cluster
    max_label = 0
    max_frequency = 0
    for idx, i in enumerate(frequency):
        if i > max_frequency:
            max_label = idx
            max_frequency = i

    # sort cluster by distance
    cluster_sorted = [max_label]
    while len(cluster_sorted) < n_cluster:
        former_cluster = cluster_sorted[-1]
        idx = 0
        min_distance = 999
        for i in range(n_cluster):
            if i not in cluster_sorted:
                distance = np.linalg.norm(centers[former_cluster] - centers[i])
                if distance < min_distance:
                    min_distance = distance
                    idx = i
        cluster_sorted.append(idx)
    # sort elements in each cluster
    res = []
    for l_idx, label in enumerate(cluster_sorted):
        # if not first cluster, then compute distance with former cluster
        if label != max_label:
            l_idx -= 1
        cluster = []
        for idx, i in enumerate(labels):
            if i == label:
                cluster.append(idx)
        res.append(sorted(cluster, key=lambda x: np.linalg.norm(n_samples[x] - centers[cluster_sorted[l_idx]])))

    return res


def allocate(cluster_sorted, g):
    '''
    allocate cluster to different groups evenly
    :param cluster_sorted: list, cluster result
    :param g: int, group number
    :return: dict, groups
    '''
    cluster_sorted = reduce(lambda x, y: x + y, cluster_sorted)
    groups = defaultdict(list)
    i = 1
    while cluster_sorted:
        if i > g:
            i %= g
        groups[i].append(cluster_sorted.pop(0))
        i += 1
    return groups


if __name__ == '__main__':

    with open('C:\\Users\Administrator.QH-20150404EHBO\PycharmProjects\\firstDjango\\upload\jsons\group_data.json', encoding='utf8') as f:
        data = json.load(f)
    names = [k for k in data]
    max_k = 5  # max cluster num to test
    X = [data[k] for k in data]
    estimators = [(i, KMeans(n_clusters=i)) for i in range(2, max_k)]

    ss = []
    labels = []
    centers = []
    max_score = -2
    cluster_num = 0
    for k, est in estimators:
        est.fit(X)
        score = round(silhouette_score(X, est.labels_), 3)
        if score > max_score:
            labels = est.labels_
            max_score = score
            centers = est.cluster_centers_
            cluster_num = est.get_params()['n_clusters']
        ss.append(score)
        plt.text(k, score, score)
        # print(k, score)
        # print(est.get_params()['n_clusters'])

    # plot silhouette score for each k
    plt.xlim([1, 10])
    plt.xlabel('k')
    plt.ylabel('silhouette score')
    plt.plot(range(2, max_k), ss, 'o-', label=ss)
    plt.savefig('silhouette_score.png')

    # plot cluster result
    plt.cla()
    color_set = ['r', 'b', 'yellow', 'green', 'black', 'brown']
    brush = random.sample(color_set, cluster_num)
    c = [brush[l] for l in labels]
    plt.scatter(list(map(lambda x: x[2], X)), list(map(lambda x: x[3], X)),
                c=c,
                s=50,
                edgecolors='black')
    for idx, i in enumerate(X):
        plt.text(i[2], i[3], idx)
    plt.savefig('best_cluster_result.png')

    # allocate groups
    clusters_sorted = sort_cluster(X, centers, labels, cluster_num)
    # print(clusters)
    groups = allocate(clusters_sorted, 3)
    res2dict = {}
    for g in groups:
        res2dict[g] = [names[i] for i in groups[g]]
        print([names[i] for i in groups[g]])
    with open('groups_result.json', 'w', encoding='utf8') as f:
        json.dump(res2dict, f, ensure_ascii=False, indent=2)