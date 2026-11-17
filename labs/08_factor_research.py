"""实验08：自动构造简单因子，比较分组收益与因子冗余。合成数据。"""
import math
import random


def corr(x,y):
    if len(x)!=len(y) or len(x)<2: raise ValueError('same length >=2 required')
    mx=sum(x)/len(x);my=sum(y)/len(y)
    cov=sum((a-mx)*(b-my) for a,b in zip(x,y))
    dx=math.sqrt(sum((a-mx)**2 for a in x));dy=math.sqrt(sum((b-my)**2 for b in y))
    return cov/dx/dy if dx*dy else 0.0


def synthetic(n=1200,seed=1):
    rng=random.Random(seed)
    obs=[]
    for i in range(n):
        oversold=rng.gauss(0,1)
        volume=rng.gauss(0,1)
        duplicate=oversold+rng.gauss(0,.04)
        future=.05*oversold+.03*oversold*volume+rng.gauss(0,.7)
        obs.append((oversold,volume,duplicate,future))
    return obs


def quintiles(xs):
    sorted_x=sorted(xs,key=lambda x:x[0]);n=len(xs)
    return [(j+1,round(sum(v for _,v in sorted_x[j*n//5:(j+1)*n//5])/(len(sorted_x[j*n//5:(j+1)*n//5])),4)) for j in range(5)]


if __name__ == '__main__':
    train=synthetic()
    a,b,c,ret=zip(*train)
    print('【合成数据】超跌因子与复制因子的相关系数：',round(corr(a,c),3))
    print('超跌因子与未来收益的相关系数：',round(corr(a,ret),3))
    print('因子5分组的未来收益均值：',quintiles(list(zip(a,ret))))
    print('挑战：把future中0.05的系数调为0，再观察变化；探索多个因子必须记下试验次数。')
