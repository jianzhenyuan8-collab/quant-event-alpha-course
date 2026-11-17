"""实验10A：无监督分类不等于预测盈利。纯Python实现一个简单二维k-means。"""
import math
import random


def distance(a,b): return sum((x-y)**2 for x,y in zip(a,b))


def kmeans(points,k=3,iters=25):
    if not 1<=k<=len(points): raise ValueError('invalid k')
    centers=[list(points[i]) for i in range(k)]
    labels=[-1]*len(points)
    for _ in range(iters):
        labels=[min(range(k),key=lambda j:distance(p,centers[j])) for p in points]
        for j in range(k):
            member=[p for p,z in zip(points,labels) if z==j]
            if member:
                centers[j]=[sum(p[d] for p in member)/len(member) for d in range(len(points[0]))]
    return centers,labels


if __name__ == '__main__':
    rng=random.Random(4)
    points=[(mx+rng.gauss(0,.2),my+rng.gauss(0,.2)) for mx,my in [(-1,1),(0,.2),(1,2)] for _ in range(100)]
    centers,labels=kmeans(points)
    print('【合成点】样本按特征分为3组，各组中心:',[(round(a,2),round(b,2)) for a,b in centers])
    print('各组样本量:',[labels.count(j) for j in range(3)])
    print('没有未来收益标签，因此不能仅凭聚类评价交易Alpha。')
