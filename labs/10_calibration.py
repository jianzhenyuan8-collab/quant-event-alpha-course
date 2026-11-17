"""实验10B：概率校准、Brier、Log Loss、精确率和召回率。"""
import math
import random


def brier(probs,ys):
    return sum((p-y)**2 for p,y in zip(probs,ys))/len(ys)


def logloss(probs,ys):
    eps=1e-12
    return -sum(y*math.log(max(eps,min(1-eps,p)))+(1-y)*math.log(max(eps,min(1-eps,1-p))) for p,y in zip(probs,ys))/len(ys)


def confusion(probs,ys,threshold=.5):
    tp=fp=fn=tn=0
    for p,y in zip(probs,ys):
        predicted=p>=threshold
        if predicted and y: tp+=1
        elif predicted and not y: fp+=1
        elif not predicted and y: fn+=1
        else: tn+=1
    return {'tp':tp,'fp':fp,'fn':fn,'tn':tn,
            'precision':tp/(tp+fp) if tp+fp else None,
            'recall':tp/(tp+fn) if tp+fn else None}


def demo(n=1000,seed=42):
    rng=random.Random(seed)
    true=[.1+.8*rng.random() for _ in range(n)]
    labels=[int(rng.random()<p) for p in true]
    return true,labels


if __name__ == '__main__':
    probs,ys=demo()
    constant=[sum(ys)/len(ys)]*len(ys)
    confident=[max(.001,min(.999,(p-.5)*1.5+.5)) for p in probs]
    for name,pred in [('知道生成概率的理想模型',probs),('恒定历史频率',constant),('过度自信的概率',confident)]:
        print('【合成事件】',name,'Brier:',round(brier(pred,ys),4),'LogLoss:',round(logloss(pred,ys),4))
    print('阈值0.7时的混淆矩阵:',confusion(probs,ys,threshold=.7))
