"""实验05：对合成5M涨跌幅定义超跌事件，计算事件后收益和简单基准。"""
RETURNS = [
    -.3,.2,.5,-1.7,.9,.4,-.2,.2,-.5,.2,-1.1,.3,.1,-.1,-.7,-1.8,
    -.7,-.4,.2,.8,.4,-.4,.3,-1.9,1.,.6,.2,-.1,-.5,.2,-.3,-1.4,
    .4,-.5,-.9,-1.6,.1,-.2,-.6,.7,.5,.1,-.8,.1,-2.,1.4,.4,-.4,
    .6,.2,-.2,.5,-1.1,.2,.3,-1.5,-.5,-.3,-.1,.7
]


def compound_percent(values):
    capital=1.0
    for r in values:
        capital*=1+r/100
    return 100*(capital-1)


def analyze(returns=RETURNS, threshold=1.6, horizon=3, cooldown=6):
    if not 0 < horizon < len(returns) or threshold <= 0 or cooldown < 0:
        raise ValueError('invalid inputs')
    indices=[]
    for i in range(len(returns)-horizon):
        if returns[i] <= -threshold and (not indices or i-indices[-1]>cooldown):
            indices.append(i)
    event=[compound_percent(returns[i+1:i+horizon+1]) for i in indices]
    baseline=[compound_percent(returns[i+1:i+horizon+1]) for i in range(len(returns)-horizon)]
    def stat(xs):
        return {'n':len(xs),'up_rate':sum(x>0 for x in xs)/len(xs) if xs else None,
                'mean_percent':sum(xs)/len(xs) if xs else None}
    return {'event_indices':indices,'event':stat(event),'baseline':stat(baseline)}


if __name__ == '__main__':
    for threshold in [0.8,1.6,2.0]:
        r=analyze(threshold=threshold)
        print(f'【合成教学数据】阈值{threshold}%, 事件{r["event"]["n"]}, 统计={r["event"]}, 全时点基准={r["baseline"]}')
    print('对照组尚未匹配趋势/波动率，不是因果结论；历史收益不等于可执行盈亏。')
