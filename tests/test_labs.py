"""仓库实验的行为检查；不请求网络，也不连接任何交易所。"""
from pathlib import Path
import importlib.util
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
LABS=ROOT/'labs'

def load(name):
    spec=importlib.util.spec_from_file_location(name,LABS/f'{name}.py')
    module=importlib.util.module_from_spec(spec)
    sys.modules[name]=module
    spec.loader.exec_module(module)
    return module

class CourseTests(unittest.TestCase):
    def test_chapters_count_and_numbering(self):
        chapters=sorted((ROOT/'chapters').rglob('*.md'))
        self.assertEqual(len(chapters),60)
        self.assertEqual(sorted(int(p.stem) for p in chapters),list(range(1,61)))
        for p in chapters:
            text=p.read_text(encoding='utf8')
            for required in ['## 1. 先从直觉理解','## 2. 把直觉变成数学','## 4. 动手练习','## 5. 自测题','## 6. 常见误区']:
                self.assertIn(required,text,p)

    def test_compound(self):
        m=load('01_compound_growth')
        self.assertAlmostEqual(m.final_wealth(1000,[-.5,.5]),750)
        self.assertAlmostEqual(m.maximum_drawdown([-.05]*10),1-.95**10)

    def test_expectancy(self):
        m=load('02_expectancy')
        self.assertAlmostEqual(m.expected_r(.4,4,0),1)
        self.assertAlmostEqual(m.breakeven_probability(4,.2),.24)
        self.assertAlmostEqual(m.position_size(10000,.01,400),.25)

    def test_binomial(self):
        m=load('04_binomial')
        self.assertAlmostEqual(m.probability_at_least(1,1,.5),.5)
        self.assertAlmostEqual(m.probability_at_least(2,1,.5),.75)

    def test_event_study(self):
        m=load('05_event_study')
        r=m.analyze()
        self.assertEqual(r['event']['n'],5)
        self.assertEqual(r['baseline']['n'],57)
        self.assertAlmostEqual(r['event']['up_rate'],.6)

    def test_multiscale(self):
        m=load('06_multiscale')
        data=m.synth_5m(36)
        self.assertEqual(len(m.aggregate_completed(data,15)),12)
        self.assertEqual(len(m.aggregate_completed(data,60)),3)
        self.assertAlmostEqual(m.aggregate_completed(data,15)[0].volume,sum(x.volume for x in data[:3]))

    def test_barrier_conservative(self):
        m=load('07_triple_barrier')
        result=m.run_long(100,98,106,[m.OHLC(100,107,97,104)],1)
        self.assertEqual(result['reason'],'stop')
        self.assertEqual(result['net_r'],-1)

    def test_rule_discovery_deterministic(self):
        m=load('09_rule_discovery')
        data=m.make_data()
        rule=m.select_rule(data[:900])
        self.assertEqual(rule,m.select_rule(data[:900]))
        self.assertIn(rule,m.candidates())
        self.assertGreater(m.evaluate(data[:900],rule)['n'],29)

    def test_calibration(self):
        m=load('10_calibration')
        self.assertAlmostEqual(m.brier([.4,.4],[1,0]),.26)
        self.assertGreater(m.logloss([.99],[0]),m.logloss([.6],[0]))

    def test_walkforward_no_overlap(self):
        m=load('11_walkforward')
        windows=list(m.walkforward_indices(400,100,50,label_horizon=5))
        self.assertTrue(windows)
        for tr,te in windows:
            self.assertLess(tr[-1]+5,te[0])

    def test_bayesian(self):
        m=load('12_bayesian_update')
        self.assertAlmostEqual(m.posterior_mean(2,1),.6)
        self.assertGreater(m.posterior_mean(100,0),m.posterior_mean(2,0))

    def test_state_machine_deduplication(self):
        m=load('13_state_machine')
        engine=m.PaperEngine()
        self.assertEqual(engine.handle('evt1','OVERSOLD'),'WATCHING')
        self.assertEqual(engine.handle('evt1','OVERSOLD'),'IGNORED_DUPLICATE')
        self.assertEqual(engine.handle('evt2','MSS'),'READY')
        self.assertEqual(engine.handle('evt3','RISK_APPROVED'),'ORDER_CREATED_NOT_FILLED')
        self.assertEqual(engine.state,'READY')
        self.assertEqual(engine.handle('evt4','FILL'),'OPEN')

    def test_report_marks_synthetic(self):
        m=load('14_research_report')
        self.assertEqual(m.report()['data_kind'],'synthetic_educational')
        with tempfile.TemporaryDirectory() as d:
            file=m.save_report(d)
            self.assertIn('虚构示例',file.read_text(encoding='utf8'))

if __name__=='__main__': unittest.main()
