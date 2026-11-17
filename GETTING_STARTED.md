# 新手快速开始：第一次运行Python实验

## 一、安装Python

访问 https://www.python.org/downloads/ 安装Python 3.10或更高版本。Windows安装时可勾选将Python加入PATH。也可以使用VS Code打开整个课程目录。

在终端输入：

```bash
python --version
```

如果使用Windows的`py`启动器，也可输入`py --version`。

## 二、先跑最简单的实验

在项目根目录打开终端：

```bash
python labs/01_compound_growth.py
```

你应该能看到先亏50%再赚50%的结果是750元。这一步完全不需要联网、币安账户或者API密钥。

## 三、运行你的第一个“超跌事件研究”

```bash
python labs/05_event_study.py
```

注意屏幕上标明：**合成教学数据**。修改`threshold`或`horizon`，运行并记录事件数量和后续平均收益的改变。

## 四、继续到自动规则发现

```bash
python labs/09_rule_discovery.py
```

你会看到机器通过过去的训练样本选择一条规则，并分别在验证集和测试集报告结果。这个实验的数据有**人工植入的规律**，不能代表真实BTC可预测。

## 五、检查整个项目

```bash
python -m unittest discover -s tests -v
```

如果出现`OK`，说明基础教学模块通过了当前单元测试；这不等于真实交易策略有效。

可选依赖：`python -m pip install -r requirements-ml.txt`，但当前16个基础实验均可只用标准库运行。
