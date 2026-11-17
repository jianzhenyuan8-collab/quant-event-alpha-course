"""实验06：将合成5分钟OHLCV聚合到15分钟和1小时，确保只使用完整窗口。"""
from dataclasses import dataclass

@dataclass(frozen=True)
class Bar:
    start_minute: int
    open: float
    high: float
    low: float
    close: float
    volume: float


def synth_5m(n=36):
    price=100.0
    data=[]
    for i in range(n):
        close=price*(1+(.002 if i%5<3 else -.001))
        data.append(Bar(5*i,price,max(price,close)*1.0005,min(price,close)*.9995,close,100+i))
        price=close
    return data


def aggregate_completed(bars, target_minutes):
    """每根输入5分钟；只允许完整且连续的目标区间进入聚合。"""
    if target_minutes%5 or target_minutes<5:
        raise ValueError('target must be a positive multiple of 5 minutes')
    n=target_minutes//5
    result=[]
    for start in range(0,len(bars),n):
        chunk=bars[start:start+n]
        if len(chunk)<n: break
        if chunk[0].start_minute%target_minutes: continue
        if any(chunk[k].start_minute!=chunk[0].start_minute+5*k for k in range(n)): continue
        result.append(Bar(chunk[0].start_minute,chunk[0].open,max(x.high for x in chunk),min(x.low for x in chunk),chunk[-1].close,sum(x.volume for x in chunk)))
    return result


if __name__ == '__main__':
    five=synth_5m()
    print('【合成OHLCV】5M根数：',len(five))
    for minutes in [15,30,60]:
        agg=aggregate_completed(five,minutes)
        print(f'{minutes}分钟聚合：{len(agg)}根，首根={agg[0]}')
    print('提示：高周期K线在整段结束时才可用于较短周期的决策。')
