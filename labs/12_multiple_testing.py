"""实验12A：在纯随机数据中搜索大量规则也会产生看似很高的相关性。"""
import math
import random


def corr(x,y):
    mx=sum(x)/len(x);my=sum(y)/len(y)
    cov=sum((a-mx)*(b-my) for a,b in zip(x,y))
    sx=math.sqrt(sum((a-mx)**2 for a in x));sy=math.sqrt(sum((b-my)**2 for b in y))
    return cov/(sx*sy) if sx*sy else 0


def max_abs_false_correlation(number_of_factors,n=100,seed=15):
    rng=random.Random(seed)
    y=[rng.gauss(0,1) for _ in range(n)]
    scores=[]
    for _ in range(number_of_factors):
        x=[rng.gauss(0,1) for _ in range(n)]
        scores.append(abs(corr(x,y)))
    return max(scores)


if __name__ == '__main__':
    for count in [10,100,1000]:
        print('【纯随机、无真实Alpha】搜索',count,'个因子的最大|相关系数|:',round(max_abs_false_correlation(count),3))
    print('挑选最优秀的训练样本因子并不证明其能预测未来。')
