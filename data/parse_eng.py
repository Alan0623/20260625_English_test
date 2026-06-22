#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re, json
raw = open('/sessions/upbeat-clever-darwin/mnt/outputs/eng_raw.txt', encoding='utf-8').read()
lines = [l for l in raw.splitlines() if not l.strip().startswith('==== PAGE')]
# drop standalone page-number lines (a lone integer)
lines = [l for l in lines if not re.fullmatch(r'\s*\d{1,3}\s*', l)]

q_start = re.compile(r'^\s*(\d+)\s*[.、]\s*[（(]\s*([A-E])\s*[）)]\s*(.*)$')
opt_inline = re.compile(r'[（(]\s*([A-E])\s*[）)]\s*(.*)')

items = []
cur = None
for line in lines:
    m = q_start.match(line)
    if m:
        if cur: items.append(cur)
        cur = {'num': int(m.group(1)), 'answer': m.group(2), 'body': [m.group(3)]}
    elif cur is not None:
        cur['body'].append(line.strip())
if cur: items.append(cur)

def parse_item(it):
    # join body, then split stem vs options
    full = '\n'.join(it['body'])
    # find option markers (A)..(D)
    marks = list(re.finditer(r'[（(]\s*([A-E])\s*[）)]', full))
    if marks:
        stem = full[:marks[0].start()].strip()
        opts = {}
        for i, mk in enumerate(marks):
            s = mk.end(); e = marks[i+1].start() if i+1 < len(marks) else len(full)
            opts[mk.group(1)] = full[s:e].strip().replace('\n',' ').strip()
    else:
        # options are the last 4 non-empty lines without letters
        parts = [p.strip() for p in full.split('\n') if p.strip()]
        opts = {}
        if len(parts) >= 4:
            optvals = parts[-4:]
            stem = ' '.join(parts[:-4]).strip()
            for L, v in zip('ABCD', optvals): opts[L] = v
        else:
            stem = full.strip()
    stem = re.sub(r'[ \t]+', ' ', stem).strip()
    return {'num': it['num'], 'stem': stem, 'options': opts, 'answer': it['answer']}

parsed = [parse_item(it) for it in items]
# quality flags
bad = [p for p in parsed if p['answer'] not in p['options'] or len(p['options']) < 2 or not p['stem']]
print('parsed:', len(parsed), 'flagged:', len(bad))
for p in bad[:15]:
    print('  num', p['num'], 'ans', p['answer'], 'opts', list(p['options'].keys()), '|', p['stem'][:50])
json.dump(parsed, open('/sessions/upbeat-clever-darwin/mnt/outputs/eng_questions.json','w',encoding='utf-8'),
          ensure_ascii=False, indent=1)
