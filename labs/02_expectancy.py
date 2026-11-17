"""实验02：R单位、盈亏平衡胜率和成本。仅教学算术模型。"""


def expected_r(win_probability: float, reward_r: float, cost_r: float = 0.0) -> float:
    if not 0 <= win_probability <= 1:
        raise ValueError('win_probability must be in [0,1]')
    if reward_r <= 0 or cost_r < 0:
        raise ValueError('reward_r must be positive and cost_r nonnegative')
    return win_probability * reward_r - (1 - win_probability) - cost_r


def breakeven_probability(reward_r: float, cost_r: float = 0.0) -> float:
    if reward_r <= 0 or cost_r < 0:
        raise ValueError('invalid reward_r or cost_r')
    return (1 + cost_r) / (reward_r + 1)


def position_size(wealth: float, risk_fraction: float, price_risk_per_unit: float, cost_per_unit: float = 0) -> float:
    if wealth <= 0 or not 0 < risk_fraction < 1 or price_risk_per_unit <= 0 or cost_per_unit < 0:
        raise ValueError('invalid parameters')
    return wealth * risk_fraction / (price_risk_per_unit + cost_per_unit)


if __name__ == '__main__':
    print('【假设模型】4R、费用0.2R，盈亏平衡胜率：', f'{breakeven_probability(4,0.2):.1%}')
    for p in [.15, .25, .4]:
        print(f'胜率{p:.0%}，每笔平均净R:', round(expected_r(p,4,0.2),3))
    print('账户1万元，每笔风险1%，每BTC价格止损400：', position_size(10000,.01,400),'BTC（未考虑费用）')
