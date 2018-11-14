from django.shortcuts import render

# Create your views here.

# 导入数据模型ArticlePost
from .models import ArticlePost
import markdown
import os

# 引入redirect重定向模块
from django.shortcuts import render, redirect
# 引入HttpResponse
from django.http import HttpResponse
# 引入刚才定义的ArticlePostForm表单类
from .forms import ArticlePostForm
# 引入User模型
from django.contrib.auth.models import User


def article_list(request):
    # 取出所有博客文章
    articles = ArticlePost.objects.all()
    # 需要传递给模板（templates）的对象
    context = {'articles': articles}
    # render函数：载入模板，并返回context对象
    return render(request, 'article/list.html', context)


import markdown


# 文章详情
def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)
    # 将markdown语法渲染成html样式
    article.body = markdown.markdown(article.body,
                                     extensions=[
                                         # 包含 缩写、表格等常用扩展
                                         'markdown.extensions.extra',
                                         # 语法高亮扩展
                                         'markdown.extensions.codehilite',
                                     ])
    context = {'article': article}
    return render(request, 'article/detail.html', context)


# 写文章的视图
def article_create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit=False)
            # 指定数据库中 id=1 的用户为作者
            new_article.author = User.objects.get(id=1)
            # 将新文章保存到数据库中
            new_article.save()
            # 完成后返回到文章列表
            return redirect("article:article_list")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文
        context = {'article_post_form': article_post_form}
        # 返回模板
        return render(request, 'article/create.html', context)


# 删文章
def article_delete(request, id):
    # 根据 id 获取需要删除的文章
    article = ArticlePost.objects.get(id=id)
    # 调用.delete()方法删除文章
    article.delete()
    # 完成删除后返回文章列表
    return redirect("article:article_list")


# 更新文章
def article_update(request, id):
    """
    更新文章的视图函数
    通过POST方法提交表单，更新titile、body字段
    GET方法进入初始表单页面
    id： 文章的 id
    """

    # 获取需要修改的具体文章对象
    article = ArticlePost.objects.get(id=id)
    # 判断用户是否为 POST 提交表单数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存新写入的 title、body 数据并保存
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect("article:article_detail", id=id)
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")

    # 如果用户 GET 请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = {'article': article, 'article_post_form': article_post_form}
        # 将响应返回到模板中
        return render(request, 'article/update.html', context)


from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from matplotlib import pyplot as plt
from collections import defaultdict
from functools import reduce
import numpy as np
import json
import random


def file_download(request,id):
    # do something...
    with open('C:\\Users\Administrator.QH-20150404EHBO\PycharmProjects\\firstDjango\\upload\jsons\group_data.json',
              encoding='utf8') as f:
        c = f.readlines()
        return HttpResponse(json.dumps(c), content_type="application/json")





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


def main():
    with open("C:\\Users\Administrator.QH-20150404EHBO\PycharmProjects\\firstDjango\\upload\jsons\group_data.json", encoding='utf8') as f:
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
        # print([names[i] for i in groups[g]])
    return res2dict
    # with open('class_result.json', 'w', encoding='utf8') as f:
    #     json.dump(res2dict, f, ensure_ascii=False, indent=2)


def file_cluster(request,id):
    res2dict = main()
    return HttpResponse(json.dumps(res2dict), content_type="application/json")



def show_result(request,id):
    with open('C:\\Users\Administrator.QH-20150404EHBO\PycharmProjects\\firstDjango\\article\groups_result.json',encoding='utf-8') as f:
        d = f.readlines()
        return HttpResponse(json.dumps(d), content_type="application/json")



def count(request,id):
    resp = {'第一组': '油梦圆', '第二组': '申泳国', '第三组': '吴晓均'}
    return HttpResponse(json.dumps(resp), content_type="application/json")

def data_acquisition(request):
    return render(request, 'article/data_acquitision.html')