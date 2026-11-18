#!/usr/bin/env python3
"""Import literal assistant lesson text from ChatGPT's official data export.

This tool does NOT summarize or rewrite. It retains assistant messages' textual
parts verbatim (including Markdown and formula syntax) and splits only on chapter
headings. Non-text UI components and media cannot be faithfully restored from
ChatGPT's JSON text export alone.
"""
import argparse
import datetime as dt
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path

CHINESE_NUMERALS = '〇零一二三四五六七八九十百两'
CHAPTER_HEADING = re.compile(
    rf'(?m)^[ \t]{{0,3}}(?:#{{1,6}}[ \t]+)?(第([{CHINESE_NUMERALS}0-9]{{1,6}})章(?:[ \t]*[：:·.—-][^\n]*)?)\s*$'
)


def numeral_to_int(s):
    if s.isdigit():
        return int(s)
    d = {'零': 0, '〇': 0, '一': 1, '二': 2, '三': 3, '四': 4,
         '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '两': 2}
    if '百' in s:
        left, right = s.split('百', 1)
        return (d.get(left, 1) if left else 1) * 100 + (numeral_to_int(right) if right else 0)
    if '十' in s:
        left, right = s.split('十', 1)
        return (d.get(left, 1) if left else 1) * 10 + (d.get(right, 0) if right else 0)
    if len(s) == 1:
        return d[s]
    raise ValueError('Not a supported chapter numeral: ' + s)


def message_text(message):
    content = message.get('content') or {}
    parts = content.get('parts') or []
    texts = []
    for p in parts:
        if isinstance(p, str):
            texts.append(p)
        elif isinstance(p, dict) and isinstance(p.get('text'), str):
            texts.append(p['text'])
    if not texts and isinstance(content.get('text'), str):
        texts.append(content['text'])
    return '\n'.join(texts)


def conversation_messages(conv):
    """Prefer the current branch of the ChatGPT message tree; fall back to sorting."""
    mapping = conv.get('mapping') or {}
    node_id = conv.get('current_node')
    chain, visited = [], set()
    while node_id and node_id in mapping and node_id not in visited:
        visited.add(node_id)
        node = mapping[node_id]
        if node.get('message'):
            chain.append(node['message'])
        node_id = node.get('parent')
    if chain:
        chain.reverse()
        return chain
    return sorted((x['message'] for x in mapping.values() if x.get('message')),
                  key=lambda m: (m.get('create_time') or 0, m.get('id') or ''))


def get_conversations(path):
    if path.suffix.lower() == '.zip':
        with zipfile.ZipFile(path) as z:
            matched = [n for n in z.namelist() if n.rsplit('/', 1)[-1] == 'conversations.json']
            if not matched:
                raise ValueError('ZIP 中找不到 conversations.json')
            with z.open(matched[0]) as f:
                return json.load(f)
    with path.open(encoding='utf-8') as f:
        return json.load(f)


def locate_conversation(items, conv_id=None, title_has=None, match_phrase=None):
    matches = []
    for conv in items:
        if conv_id and conv.get('id') != conv_id:
            continue
        if title_has and title_has.lower() not in (conv.get('title') or '').lower():
            continue
        if match_phrase:
            messages = conversation_messages(conv)
            if not any(match_phrase in message_text(m) for m in messages):
                continue
        matches.append(conv)
    if len(matches) != 1:
        names = [f"{x.get('id')}  {x.get('title')}" for x in matches[:15]]
        raise ValueError(
            f'找到 {len(matches)} 个匹配的对话，请使用 --conversation-id 精确指定。\n' +
            ('\n'.join(names) if names else '没有匹配的对话；可尝试 --list。')
        )
    return matches[0]


def collect_assistant_chapters(conv, min_chapter=1, max_chapter=60):
    chapters, unmatched = {}, []
    for message in conversation_messages(conv):
        if (message.get('author') or {}).get('role') != 'assistant':
            continue
        content = message_text(message)
        if not content.strip():
            continue
        matches = list(CHAPTER_HEADING.finditer(content))
        if not matches:
            if '从零理解我们的交易数学模型' in content or '第60章' in content:
                unmatched.append(message.get('id') or '')
            continue
        for i, match in enumerate(matches):
            number = numeral_to_int(match.group(2))
            if number < min_chapter or number > max_chapter:
                continue
            end = matches[i+1].start() if i+1 < len(matches) else len(content)
            excerpt = content[match.start():end].rstrip()
            if excerpt:
                chapters.setdefault(number, []).append({
                    'message_id': message.get('id'),
                    'create_time': message.get('create_time'),
                    'text': excerpt,
                    'original_heading': match.group(1),
                })
    return chapters, unmatched


def write_archive(conv, chapters, outdir, overwrite=False):
    outdir = Path(outdir)
    if outdir.exists() and any(outdir.iterdir()) and not overwrite:
        raise ValueError(f'输出文件夹已有内容：{outdir}；请另选 --out 或添加 --overwrite')
    outdir.mkdir(parents=True, exist_ok=True)
    manifest = []
    for number in sorted(chapters):
        entries = chapters[number]
        header = [
            f'<!-- 来源：ChatGPT 对话导出，conversation id: {conv.get("id") or "unknown"} -->',
            '<!-- 内容：原助手消息文本直接提取；未做摘要或语义改写。 -->',
            '<!-- 注意：原消息中的交互控件、图片等可能无法作为文本恢复。 -->',
            '',
        ]
        for i, e in enumerate(entries):
            if i:
                header.append('\n---\n\n> 说明：同一章在另一个助手消息中出现，以下保留原始版本，不覆盖上段。\n')
            header.append(e['text'])
        target = outdir / f'{number:02d}.md'
        target.write_text('\n'.join(header).rstrip() + '\n', encoding='utf-8')
        manifest.append({'chapter': number, 'filename': target.name,
                         'message_ids': [e['message_id'] for e in entries],
                         'char_count': sum(len(e['text']) for e in entries),
                         'repetitions': len(entries)})
    (outdir / 'manifest.json').write_text(json.dumps({
        'source': 'ChatGPT official conversations.json export',
        'conversation_id': conv.get('id'), 'conversation_title': conv.get('title'),
        'chapters': manifest, 'missing_chapters': [i for i in range(1, 61) if i not in chapters],
    }, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (outdir / 'README.md').write_text(
        '# 聊天记录原文归档\n\n'
        '本文件夹通过 `scripts/import_chatgpt_export.py` 从用户自行导出的 ChatGPT `conversations.json` 自动生成。'
        '**没有重新总结、简写或改写助手正文**，仅依据章节标题拆分并添加来源注释。\n\n'
        f'来源会话：`{conv.get("title")}`，会话ID：`{conv.get("id")}`。\n\n'
        f'已恢复章节：{len(manifest)} / 60。缺失章节：'
        + ', '.join(str(i) for i in range(1, 61) if i not in chapters)
        + '。\n\n注意：官方导出中若包含结构化交互控件、图片或其他非文本内容，'
        '不能保证这些内容原样转为 Markdown。公开前请自行检查个人信息。\n', encoding='utf-8')
    return manifest


def main():
    parser = argparse.ArgumentParser(description='从 ChatGPT 官方数据导出中恢复课程原文（不改写）')
    parser.add_argument('export', type=Path, help='官方导出的 .zip 或 conversations.json 文件')
    parser.add_argument('--conversation-id', help='精确指定会话ID')
    parser.add_argument('--title-has', help='仅匹配标题包含指定文本的会话')
    parser.add_argument('--match-phrase', help='匹配会话消息内的文本；如果有多个结果需指定会话ID')
    parser.add_argument('--out', default='chat-original', help='输出目录；默认 chat-original')
    parser.add_argument('--overwrite', action='store_true', help='允许覆盖指定输出目录中的章节文件')
    parser.add_argument('--list', action='store_true', help='只列出导出文件中的对话标题和ID，不写文件')
    args = parser.parse_args()
    conversations = get_conversations(args.export)
    if args.list:
        for c in conversations:
            print(f"{c.get('id')}\t{c.get('title')}")
        return 0
    conv = locate_conversation(conversations, args.conversation_id,
                               args.title_has, args.match_phrase)
    chapters, unmatched = collect_assistant_chapters(conv)
    if not chapters:
        print('未发现符合格式的章节标题。请检查选中的会话和原消息格式。', file=sys.stderr)
        return 2
    manifest = write_archive(conv, chapters, args.out, args.overwrite)
    print(f'已归档：{len(manifest)} 章；文件夹：{args.out}')
    print('未恢复章节：', ', '.join(str(x) for x in range(1, 61) if x not in chapters) or '无')
    print('注意：公开发布前，请先检查导出内容是否含有个人信息。')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
