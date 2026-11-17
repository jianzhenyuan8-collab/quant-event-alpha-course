"""实验01：复利与回撤。仅标准库；纯教学假设，不使用真实行情。"""
import math


def final_wealth(initial: float, returns: list[float]) -> float:
    """returns为账户收益率，例如0.2、-0.05。"""
    value = initial
    for r in returns:
        if r <= -1:
            return 0.0
        value *= 1 + r
    return value


def maximum_drawdown(returns: list[float]) -> float:
    wealth = peak = 1.0
    worst = 0.0
    for r in returns:
        wealth *= 1 + r
        peak = max(peak, wealth)
        worst = max(worst, 1 - wealth / peak)
    return worst


if __name__ == '__main__':
    print('【合成教学数据】复利实验')
    print('先亏50%再赚50%：', final_wealth(1000, [-0.5, 0.5]))
    print('连续42笔+20%的财富倍数：', round(final_wealth(1, [0.2]*42), 2))
    print('10笔连续-5%的回撤：', f'{maximum_drawdown([-0.05]*10):.2%}')
    print('达到10倍、每笔+5%的理想化获胜次数：', math.ceil(math.log(10)/math.log(1.05)))
    print('挑战：修改[-0.5, 0.5]为[-0.2, 0.2]，看看为何不能抵消。')
