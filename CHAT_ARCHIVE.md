# 60章聊天原文归档计划与来源说明

## 现有状态

- [`chapters/`](chapters/) 是**重新整理的精简教材版**，不是对话原文。**保留不动**，方便快速复习。
- [`chat-original/`](chat-original/) 专用于保存从 ChatGPT 官方导出中提取的**原助手消息正文**。不会用重新写的文章冒充聊天记录原文。
- [`chat-excerpts/`](chat-excerpts/) 存放当前可核对的聊天教学片段，明确标明为摘录，**不是完整对话导出**。
- 目前还没有取得 ChatGPT 官方对话 JSON，因此**不能宣称已经上传60章逐字原文**。这是对上一版内容过度简化问题的明确修正。

## 为什么不直接把旧版教材重命名成原文？

原聊天的详尽讲解包含例子、推理过程和交互式练习。旧版教材是重新总结与改写的成果，无法保留每一条原始表述。若仅把旧教材放进 `chat-original/`，会破坏来源的可信度。

## 使用官方导出恢复原文

1. 在 ChatGPT 的 **设置 → 数据控制 → 导出数据** 获取官方导出 ZIP。ZIP 中应含 `conversations.json`。
2. 解压或直接使用 ZIP。不要把完整 ZIP 上传公开仓库：它可能包含所有聊天和私人数据。
3. 本地运行：

```bash
python scripts/import_chatgpt_export.py path/to/chatgpt-export.zip --list
python scripts/import_chatgpt_export.py path/to/chatgpt-export.zip --conversation-id YOUR_CONVERSATION_ID --out chat-original
```

4. 查看 `chat-original/manifest.json`，核实每章对应的消息ID和缺失章节。**逐章检查内容与个人信息**；确定无误后再提交。
5. 直接提交生成的章节 Markdown，不提交 `conversations.json` 或官方 ZIP。

重要说明：若若干章节原本在同一条助手回复中，导入器会按照章节标题拆分。若存在编辑过的分支，会优先按当前消息链恢复。ChatGPT 富文本交互控件、实时组件与图片未必能通过 JSON 完整恢复；导入器保留可恢复的文本和公式，不凭空生成缺失内容。

## 版本保护与回滚

公开仓库主分支名 `main`。上传前的原始教材版本有**固定备份分支**：

[`archive/pre-chat-transcript-2026-11-19`](https://github.com/jianzhenyuan8-collab/quant-event-alpha-course/tree/archive/pre-chat-transcript-2026-11-19)

备份提交：`02ae8536b06dcc47e85f58a68dfe62a4fd7c8567`。

恢复某次修改，建议使用 `git revert <该次提交SHA>` 创建一个可审计的反向提交；如需查看旧版，可直接切换到备份分支。**不建议强制推送重写公开 `main` 的历史**。后续每批原文补档都应独立提交，便于分批回滚。

## 隐私与安全

这个仓库是 **Public**。原对话可能提到真实交易仓位、账号、地址、个人研究、密钥或资金信息。上传前必须审查；不要提交交易所API密钥、助记词、钱包私钥、全部对话导出文件或未经审查的个人信息。
