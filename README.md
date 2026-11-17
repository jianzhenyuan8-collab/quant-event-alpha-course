# 从零理解量化研究：市场事件、Alpha 与机器学习（60章）

> **给高中数学基础的学习者** · 从复利开始，一步步学习事件研究、因子分析、Alpha、机器学习、决策与事件驱动执行。

本仓库是对连续60章课程的**教材化整理与扩写版**：保留每一章的核心概念、教学例子和递进顺序，加入独立Markdown章节、可运行实验、练习答案、研究报告模板以及自动测试。不是聊天记录逐字备份。

**没有任何自动实盘下单代码。默认使用合成/教学数据，不需要交易所API Key。** 教学示例中的胜率和收益与真实BTC表现无关。

## 开始学习

- [阅读完整60章目录](SYLLABUS.md)
- [查看16个动手实验](LABS.md)
- [三种学习路线](LEARNING_PATHS.md)
- [新手快速上手](GETTING_STARTED.md)
- [60章打卡进度](PROGRESS.md)
- [数据与伦理说明](data/README.md)
- [体系架构](docs/ARCHITECTURE.md)
- [实验记录模板](notes/EXPERIMENT_TEMPLATE.md)
- [本仓库内容说明](notes/EDITORIAL_NOTE.md)

## 如何运行实验

需要 Python 3.10+。目前全部16个实验均可只使用 Python 标准库运行；`numpy`、`pandas`、`scikit-learn` 放在可选依赖中，为今后接入大型真实数据准备。

```bash
python labs/01_compound_growth.py
python labs/05_event_study.py
python labs/07_triple_barrier.py
python labs/09_rule_discovery.py
python -m unittest discover -s tests -v
```

选装机器学习依赖：

```bash
python -m pip install -r requirements-ml.txt
```

## 建议学习节奏

每次选择一章，先试着口头回答“核心问题”，再阅读直觉与公式，运行实验，改动一个参数，最后用[实验模板](notes/EXPERIMENT_TEMPLATE.md)记录三个内容：**观察、解释、尚未验证的疑问**。

1—12章是数学与风险基础；13—33章是事件与统计基础；34—49章建立机器学习及Alpha意识；50—60章讨论决策和系统工程。

## 项目边界

- **发现市场现象 ≠ 证明未来可预测 ≠ 存在可交易Alpha**。
- 所有例子遵循只用决策时已知数据的原则；真正市场回测还需处理费用、资金费率、标记价格、滑点、强平与样本外验证。
- 除特别说明，实验数据是**合成/教学数据**，不会宣称为2023—2026年BTC真实回测。
- BTC属于高风险市场，杠杆可能在触及计划止损前触发强平。本项目仅用于研究和教育，不构成投资建议。

## 目录结构

```text
chapters/       60个独立Markdown章节（7个单元）
labs/           16个可运行实验脚本
tests/          自动化检查和基础测试
notes/          学习笔记和研究模板
docs/           数据流、验证与执行隔离架构
data/           数据格式说明（默认不包含交易所历史数据）
.github/        GitHub Actions测试工作流
```

## 学习成果

完成本课程后，应该能用自己的话说明：什么是R、期望对数增长、市场事件、特征与标签、条件概率、因子与Alpha、样本外验证、概率校准、事件状态机，并独立完成一个**带基准、明确数据来源、可重复运行**的小型研究。

## 版权与使用

本项目按课程学习资料组织；没有转录第三方受版权保护的资料。仓库默认未指定开源许可证，创建者可自行选择公开方式及许可证。
