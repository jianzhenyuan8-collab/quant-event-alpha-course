"""实验12B：Beta-Bernoulli先验/后验均值，只适合独立、固定胜率的简化模型。"""


def posterior_mean(wins,losses,a=1,b=1):
    if min(wins,losses)<0 or min(a,b)<=0: raise ValueError('invalid inputs')
    return (a+wins)/(a+b+wins+losses)


if __name__ == '__main__':
    for wins,losses in [(0,0),(2,0),(2,1),(100,0),(40,60)]:
        print(f'【独立事件假设】胜{wins}负{losses}：历史成功率=',round(wins/(wins+losses),3) if wins+losses else '无样本',
              'Beta(1,1)后验均值=',round(posterior_mean(wins,losses),3))
    print('真实市场有状态变化，不应把所有历史事件视为相同分布。')
