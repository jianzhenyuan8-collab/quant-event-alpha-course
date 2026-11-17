"""实验04：二项概率与抽样不确定性。"""
from math import comb


def probability_at_least(n: int, success_at_least: int, p: float) -> float:
    if n < 0 or not 0 <= p <= 1:
        raise ValueError('invalid inputs')
    return sum(comb(n, k) * p**k * (1-p)**(n-k) for k in range(max(0, success_at_least), n+1))


def approximate_ci(p: float,n: int):
    if n < 1:
        raise ValueError('need n>=1')
    e=1.96*(p*(1-p)/n)**.5
    return max(0,p-e),min(1,p+e)


if __name__ == '__main__':
    print('【独立试验教学模型】20笔、胜率40%，至少10胜概率：',f'{probability_at_least(20,10,.4):.2%}')
    for n in [10,100,1000]:
        print(f'历史成功率40%，样本{n}个，独立二项近似区间：{approximate_ci(.4,n)}')
    print('金融事件相互重叠时，上述区间不能原样应用。')
