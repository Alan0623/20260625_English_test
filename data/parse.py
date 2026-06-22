#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re, json

raw = open('/sessions/upbeat-clever-darwin/mnt/outputs/raw.txt', encoding='utf-8').read()

# normalize full-width letters
def normletter(s):
    return s.translate(str.maketrans('ＡＢＣＤＥ', 'ABCDE'))

lines = raw.splitlines()
# strip page markers
lines = [l for l in lines if not l.strip().startswith('==== PAGE')]

# patterns
q_start = re.compile(r'^\s*(\d+)\s*[\.、]\s*[（(]\s*([A-EＡ-Ｅ])\s*[）)]\s*(.*)$')
cn_nums = '一二三四五六七八九十'
# passage header: starts with chinese numeral followed by 、
passage_hdr = re.compile(r'^\s*([一二三四五六七八九十]+)\s*、\s*(.*)$')
section_hdr = re.compile(r'^\s*(請[仔計].*|邏輯測驗)\s*$')

items = []          # list of question dicts
cur = None          # current question being built
cur_passage = None  # current passage text (for reading-comp groups)
passage_buf = None  # accumulating passage lines
mode = 'normal'
sec = -1            # section index (incremented at each section header)

def flush_q():
    global cur
    if cur is not None:
        items.append(cur)
        cur = None

for raw_line in lines:
    line = raw_line.rstrip()
    if not line.strip():
        # blank: if building passage, keep; else continuation no-op
        if passage_buf is not None:
            pass
        continue

    m_sec = section_hdr.match(line)
    if m_sec:
        flush_q()
        cur_passage = None
        passage_buf = None
        if '邏輯測驗' not in line:   # the bare title isn't a content section
            sec += 1
        continue

    m_pass = passage_hdr.match(line)
    # Only treat as passage header if it's a real CN-numeral group header
    # (avoid matching question continuation). Heuristic: line doesn't start with digit.
    if m_pass and not re.match(r'^\s*\d', line):
        flush_q()
        # start new passage; accumulate following non-question lines
        cur_passage = None
        passage_buf = [m_pass.group(2).strip()] if m_pass.group(2).strip() else []
        # mark that we're collecting passage context
        cur_passage = '__COLLECTING__'
        continue

    m_q = q_start.match(line)
    if m_q:
        # finalize passage collection
        if cur_passage == '__COLLECTING__':
            cur_passage = ' '.join(x for x in passage_buf if x).strip() if passage_buf else ''
            passage_buf = None
        flush_q()
        num = int(m_q.group(1))
        ans = normletter(m_q.group(2))
        body = m_q.group(3)
        cur = {'num': num, 'answer': ans, 'body_lines': [body], 'sec': sec,
               'passage': cur_passage if cur_passage and cur_passage != '__COLLECTING__' else ''}
        continue

    # continuation line
    if cur_passage == '__COLLECTING__':
        # still collecting passage context (between header and first sub-question)
        passage_buf.append(line.strip())
        continue
    if cur is not None:
        cur['body_lines'].append(line.strip())
    # else: stray line, ignore

flush_q()

# --- fixup: merge OCR-split question (25 "天將降大任" whose options spilled into a bogus "26") ---
for i, it in enumerate(items):
    body = '\n'.join(it['body_lines'])
    if it['num'] == 25 and '將天大任' in body and i+1 < len(items):
        nxt = items[i+1]
        if nxt['num'] == 26 and '將' in '\n'.join(nxt['body_lines']):
            it['body_lines'].append('(B)' + '\n'.join(nxt['body_lines']))
            items.pop(i+1)
            break

# Now parse options from body
opt_marker = re.compile(r'[（(]\s*([A-EＡ-Ｅ])\s*[）)]')

parsed = []
problems = []
for it in items:
    body = '\n'.join(it['body_lines'])
    # find option markers
    markers = list(opt_marker.finditer(body))
    if markers:
        stem = body[:markers[0].start()].strip()
        opts = []
        for i, mk in enumerate(markers):
            start = mk.end()
            end = markers[i+1].start() if i+1 < len(markers) else len(body)
            txt = body[start:end].strip()
            opts.append(txt)
    else:
        stem = body.strip()
        opts = []
    # assign options positionally to A,B,C,...
    letters = ['A','B','C','D','E','F']
    options = {}
    for i, txt in enumerate(opts):
        if i < len(letters):
            options[letters[i]] = txt
    # clean stem: collapse text-wrap newlines to space; keep grid-row newlines
    gridrow = re.compile(r'^[\d\s\?\-\+xX×÷=≦≧<>≤≥\.\(\)/]+$')
    raw_lines_stem = stem.split('\n')
    out = raw_lines_stem[0]
    for ln in raw_lines_stem[1:]:
        if gridrow.match(ln.strip()) and ln.strip():
            out += '\n' + ln.strip()
        else:
            out += ' ' + ln.strip()
    stem_clean = re.sub(r'[ \t]+', ' ', out).strip()
    q = {
        'num': it['num'],
        'sec': it.get('sec', -1),
        'passage': re.sub(r'[ \t]+',' ', it['passage']).strip(),
        'stem': stem_clean,
        'options': options,
        'answer': it['answer'],
    }
    parsed.append(q)
    # flag problems
    if it['answer'] not in options or len(options) < 2 or not stem_clean:
        problems.append(q)

print('total parsed questions:', len(parsed))
print('flagged problems:', len(problems))
json.dump(parsed, open('/sessions/upbeat-clever-darwin/mnt/outputs/questions.json','w',encoding='utf-8'),
          ensure_ascii=False, indent=1)
json.dump(problems, open('/sessions/upbeat-clever-darwin/mnt/outputs/problems.json','w',encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('--- first 3 problems ---')
for p in problems[:8]:
    print(p['num'], '|ans',p['answer'],'|opts',list(p['options'].keys()),'|stem:', p['stem'][:50])
