"""No third-party dependencies: python -m unittest discover -s tests -v"""
import importlib.util
import tempfile
import unittest
import json
from pathlib import Path

p=Path(__file__).parents[1]/'scripts'/'import_chatgpt_export.py'
spec=importlib.util.spec_from_file_location('course_chat_importer',p)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class ExportImportTests(unittest.TestCase):
    def test_numerals(self):
        self.assertEqual(mod.numeral_to_int('一'),1)
        self.assertEqual(mod.numeral_to_int('十二'),12)
        self.assertEqual(mod.numeral_to_int('二十六'),26)
        self.assertEqual(mod.numeral_to_int('五十九'),59)
        self.assertEqual(mod.numeral_to_int('六十'),60)
    def sample(self):
        parts=['## 第一章：为什么复利是乘法？\n公式 $W=W_0(1+r)^n$。\n实验：计算收益。',
               '## 第二章：何谓 R？\n实际数学公式：$E=pb-(1-p)$。\n\n## 第三章：风险\n不会丢失的内容！']
        mapping={}
        last=None
        for i,txt in enumerate(parts):
            node=f'node-{i}'
            mapping[node]={'parent':last,'message':{'id':f'msg-{i}', 'author':{'role':'assistant'},
                       'create_time':float(i), 'content':{'content_type':'text','parts':[txt]}}}
            last=node
        return {'id':'course-id','title':'建立交易模型','mapping':mapping,'current_node':last}
    def test_extract_and_preserve_text(self):
        chapters,_=mod.collect_assistant_chapters(self.sample())
        self.assertEqual(sorted(chapters),[1,2,3])
        self.assertIn('$W=W_0(1+r)^n$',chapters[1][0]['text'])
        self.assertIn('不会丢失的内容！',chapters[3][0]['text'])
        with tempfile.TemporaryDirectory() as temp:
            manifest=mod.write_archive(self.sample(),chapters,Path(temp)/'out')
            self.assertEqual(len(manifest),3)
            self.assertIn('实际数学公式', (Path(temp)/'out'/'02.md').read_text())
            self.assertTrue((Path(temp)/'out'/'manifest.json').is_file())
    def test_current_branch_wins(self):
        sample=self.sample()
        sample['mapping']['other']={'parent':'node-0','message':{'id':'branch', 'author':{'role':'assistant'},
                            'content':{'parts':['## 第三十章：不应出现的旧分支']}}}
        chapters,_=mod.collect_assistant_chapters(sample)
        self.assertNotIn(30,chapters)
    def test_no_user_messages(self):
        sample=self.sample()
        sample['mapping']['node-1']['message']['author']['role']='user'
        chapters,_=mod.collect_assistant_chapters(sample)
        self.assertEqual(sorted(chapters),[1])

if __name__=='__main__':
    unittest.main()
