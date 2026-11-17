"""实验13：事件驱动的纸面订单状态机。无真实交易所连接。"""
from dataclasses import dataclass,field

@dataclass
class PaperEngine:
    state: str='WAITING'
    seen_ids: set=field(default_factory=set)
    orders: dict=field(default_factory=dict)

    def handle(self,event_id,event_type,expired=False):
        if event_id in self.seen_ids: return 'IGNORED_DUPLICATE'
        self.seen_ids.add(event_id)
        if expired: return 'IGNORED_EXPIRED'
        if event_type=='OVERSOLD' and self.state=='WAITING':
            self.state='WATCHING';return 'WATCHING'
        if event_type=='MSS' and self.state=='WATCHING':
            self.state='READY';return 'READY'
        if event_type=='RISK_APPROVED' and self.state=='READY':
            self.orders[event_id]='CREATED';return 'ORDER_CREATED_NOT_FILLED'
        if event_type=='FILL' and self.orders:
            last=list(self.orders)[-1]
            if self.orders[last]!='FILLED':
                self.orders[last]='FILLED';self.state='OPEN';return 'OPEN'
        if event_type=='EXIT' and self.state=='OPEN':
            self.state='CLOSED';return 'CLOSED'
        return 'NO_STATE_CHANGE'


if __name__=='__main__':
    eng=PaperEngine()
    for uid,event in [('e1','OVERSOLD'),('e2','MSS'),('e3','RISK_APPROVED'),('e3','RISK_APPROVED'),('e4','FILL'),('e5','EXIT')]:
        print(event,uid,'=>',eng.handle(uid,event),'state=',eng.state,'orders=',eng.orders)
    print('本例只演示状态与幂等机制，不验证真实订单、风险或资金。')
