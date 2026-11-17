"""实验11：纯时间滚动切分，带预测窗口的清除区间，防止标签跨越测试起点。"""


def walkforward_indices(n,train_size,test_size,label_horizon=0,step=None):
    if min(n,train_size,test_size)<=0 or label_horizon<0:
        raise ValueError('invalid sizes')
    step=step or test_size
    k=0
    while True:
        train_start=k*step
        test_start=train_start+train_size
        test_end=test_start+test_size
        if test_end>n: break
        # 训练i对应的标签可能覆盖 i+label_horizon，必须严格早于测试起点
        train_end=max(train_start,test_start-label_horizon)
        train=list(range(train_start,train_end))
        test=list(range(test_start,test_end))
        if train and test: yield train,test
        k+=1


if __name__ == '__main__':
    print('【教学时间索引】总长度400；训练100、测试50、标签覆盖未来5根')
    for i,(train,test) in enumerate(walkforward_indices(400,100,50,label_horizon=5)):
        print('轮次',i+1,'训练',train[0],'~',train[-1],'测试',test[0],'~',test[-1],
              '不泄漏:',train[-1]+5<test[0])
