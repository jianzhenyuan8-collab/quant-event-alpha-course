"""实验03：固定胜率/盈亏比下模拟多条账户曲线；不代表真实市场预测。"""
import math
import random


def simulate_paths(n_paths: int = 2000, n_trades: int = 100, win_rate: float = .4, reward_r: float = 4, risk: float = .01, seed: int = 42):
    rng = random.Random(seed)
    wealths, drawdowns = [], []
    for _ in range(n_paths):
        wealth = peak = 1.0
        worst = 0.0
        for _ in range(n_trades):
            ret = risk * (reward_r if rng.random() < win_rate else -1)
            wealth *= (1 + ret)
            peak = max(peak, wealth)
            worst = max(worst, 1 - wealth / peak)
        wealths.append(wealth)
        drawdowns.append(worst)
    return sorted(wealths), sorted(drawdowns)


def quantile(sorted_data, q):
    return sorted_data[min(len(sorted_data)-1, int(q*(len(sorted_data)-1)))]


if __name__ == '__main__':
    w, dd=simulate_paths()
    print('【合成蒙特卡洛】固定胜率40%、赢4R/输1R、每笔风险1%、100笔')
    print('最终账户倍数的10%/50%/90%分位：', *(round(quantile(w,k),3) for k in [.1,.5,.9]))
    print('最大回撤中位数：', f'{quantile(dd,.5):.2%}')
    print('理论单笔对数增长：',round(.4*math.log(1.04)+.6*math.log(.99),5))
    print('改变seed或risk，观察不同路径与回撤。市场交易通常并非独立同分布。')
