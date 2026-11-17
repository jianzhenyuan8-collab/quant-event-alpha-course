"""实验14：生成带数据性质与限制说明的Markdown+JSON研究卡片。只使用合成例子。"""
import json
from pathlib import Path


def report():
    event_n=120;success=36;baseline_success=.25
    return {
        'id':'SYNTH-EVENT-001', 'data_kind':'synthetic_educational',
        'event':'5M超跌 + 15M扫荡（虚构定义）',
        'event_count':event_n,'event_success_count':success,'event_rate':success/event_n,
        'baseline_rate':baseline_success,
        'out_of_sample':'NOT_TESTED','transaction_costs':'NOT_MODELED',
        'conclusion':'仅发现合成样本关联，不证明真实交易Alpha',
        'warnings':['不能当作BTC历史真实结果','没有独立样本外检验','未纳入成交与强平']
    }


def save_report(outdir):
    d=Path(outdir);d.mkdir(parents=True,exist_ok=True)
    obj=report()
    (d/'research_example.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf8')
    (d/'research_example.md').write_text(
        '# '+obj['id']+' · 自动事件研究报告（虚构示例）\n\n'
        f'**数据类别：{obj["data_kind"]}**\n\n事件：{obj["event"]}\n\n'
        f'样本数：{obj["event_count"]}；成功：{obj["event_success_count"]}；比例：{obj["event_rate"]:.1%}；'
        f'基准：{obj["baseline_rate"]:.1%}\n\n样本外：{obj["out_of_sample"]}\n\n'
        f'成本：{obj["transaction_costs"]}\n\n结论：{obj["conclusion"]}\n\n'
        '## 限制\n\n'+''.join('- '+v+'\n' for v in obj['warnings'])
        ,encoding='utf8')
    return d/'research_example.md'


if __name__=='__main__':
    print('【合成教学报告】已生成:',save_report('results'))
