"""实验07：三重障碍与路径顺序。单个观察条内双触及保守计为止损。"""
from dataclasses import dataclass

@dataclass(frozen=True)
class OHLC:
    open: float
    high: float
    low: float
    close: float


def run_long(entry, stop, target, future_bars, max_bars, cost_r=0):
    if not (stop < entry < target) or max_bars<=0:
        raise ValueError('invalid levels or max_bars')
    for elapsed,bar in enumerate(future_bars[:max_bars],1):
        if bar.open<stop: # 跳空低开，实际可能更差；只用开盘价做简单保守近似
            exit_price=bar.open
            return {'reason':'gap_stop','bars':elapsed,'net_r':(exit_price-entry)/(entry-stop)-cost_r}
        if bar.low<=stop:
            return {'reason':'stop','bars':elapsed,'net_r':-1-cost_r}
        if bar.high>=target:
            return {'reason':'target','bars':elapsed,'net_r':(target-entry)/(entry-stop)-cost_r}
    if len(future_bars)<max_bars:
        raise ValueError('insufficient future bars for time exit')
    return {'reason':'time','bars':max_bars,'net_r':(future_bars[max_bars-1].close-entry)/(entry-stop)-cost_r}


if __name__ == '__main__':
    paths={
        '先止损再反弹':[OHLC(100,101,97,99),OHLC(99,106,98,106)],
        '先止盈':[OHLC(100,106.5,99,106),OHLC(106,107,105,106)],
        '同根双触及':[OHLC(100,107,97,104),OHLC(104,105,103,104)],
        '时间退出':[OHLC(100,101,99,100.5),OHLC(100.5,101.5,99.5,100.8)]
    }
    for name,bars in paths.items():
        print('【合成路径】',name,run_long(100,98,106,bars,2,cost_r=.1))
    print('挑战：修改目标106为108，比较触及率；真实OHLC无法判定同根内部先后。')
