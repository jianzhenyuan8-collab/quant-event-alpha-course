"""实验09：搜索候选阈值，并且只能在过去训练集选规则，在未来测试集验证。"""
import random


def make_data(n=1500,seed=1):
    rng=random.Random(seed)
    records=[]
    for i in range(n):
        drop=rng.uniform(0,3)
        vol=rng.uniform(.5,4)
        # 人为植入的稳定事件后成功机制；并非真实BTC
        true_prob=.18+(.45 if drop>1.6 and vol>2.2 else 0)
        outcome=int(rng.random()<true_prob)
        records.append((drop,vol,outcome))
    return records


def candidates():
    return [(round(d*.2,2),round(v*.25,2)) for d in range(5,14) for v in range(4,15)]


def evaluate(data,condition):
    d,v=condition
    selected=[y for drop,vol,y in data if drop>d and vol>v]
    if not selected: return {'n':0,'rate':None}
    return {'n':len(selected),'rate':sum(selected)/len(selected)}


def select_rule(data,min_events=30):
    scored=[]
    for c in candidates():
        info=evaluate(data,c)
        if info['n']>=min_events:
            scored.append((info['rate'],info['n'],c))
    if not scored: raise ValueError('no candidate has enough examples')
    return max(scored,key=lambda x:(x[0],x[1]))[2]


if __name__ == '__main__':
    data=make_data()
    train,valid,test=data[:900],data[900:1200],data[1200:]
    chosen=select_rule(train)
    print('【合成/植入机制】自动选择规则：下跌强度 >',chosen[0],'且成交量异常比 >',chosen[1])
    print('候选规则数量：',len(candidates()))
    for label,block in [('训练',train),('验证',valid),('测试',test)]:
        print(label, evaluate(block,chosen),'全量成功率:',round(sum(x[2] for x in block)/len(block),3))
    print('测试区间只用于汇报，不用于本轮重新选择阈值。')
