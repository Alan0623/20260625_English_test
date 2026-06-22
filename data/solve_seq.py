#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""數列推理自動解題器:偵測規律、驗證能否推出標示答案,產生解說。"""
import json, re
from fractions import Fraction

qs = json.load(open('/sessions/upbeat-clever-darwin/mnt/outputs/questions.json', encoding='utf-8'))
seq = [q for q in qs if q['sec'] == 3]

def parse_terms(stem):
    # take part before any '(' option marker; split by ，or ,
    s = stem
    toks = re.split(r'[，,]', s)
    terms = []
    blank = None
    for t in toks:
        t = t.strip().strip('。').strip()
        if t == '': continue
        if '___' in t or '＿' in t or t == '?' or t == '？':
            terms.append(None);
            if blank is None: blank = len(terms)-1
        else:
            m = re.fullmatch(r'-?\d+', t)
            if m: terms.append(int(t))
            else: return None, None  # non-numeric -> not handled here
    if blank is None: return None, None
    return terms, blank

def vals_known(terms):
    return [(i,v) for i,v in enumerate(terms) if v is not None]

def try_arith(terms, b):
    kv=[v for v in terms if v is not None]
    if len(kv)<3: return None
    idxs=[i for i,v in enumerate(terms) if v is not None]
    d=terms[idxs[1]]-terms[idxs[0]]
    # need contiguous-ish; compute assuming arithmetic across full index
    # estimate first term a0
    a0=terms[idxs[0]]-d*idxs[0]
    ok=all(terms[i]==a0+d*i for i in idxs)
    if not ok: return None
    pred=a0+d*b
    return pred, f"這是等差數列,每一項都比前一項多 {d};因此空格 = {a0+d*(b-1) if b>0 else a0} {'+' if d>=0 else '−'} {abs(d)} = {pred}。"

def try_geom(terms,b):
    idxs=[i for i,v in enumerate(terms) if v is not None]
    if len(idxs)<3: return None
    if terms[idxs[0]]==0: return None
    r=Fraction(terms[idxs[1]],terms[idxs[0]])
    a0=Fraction(terms[idxs[0]])/ (r**idxs[0])
    try:
        ok=all(Fraction(terms[i])==a0*(r**i) for i in idxs)
    except ZeroDivisionError:
        return None
    if not ok: return None
    pred=a0*(r**b)
    if pred.denominator!=1: return None
    rr = f"{r.numerator}/{r.denominator}" if r.denominator!=1 else str(r.numerator)
    return int(pred), f"這是等比數列,每一項都是前一項的 {rr} 倍;故空格 = {pred}。"

def try_2nd(terms,b):
    # need consecutive known terms to compute differences; assume full sequence numeric except blank
    if any(v is None for i,v in enumerate(terms) if i!=b): return None
    n=len(terms)
    known=[(i,terms[i]) for i in range(n) if i!=b]
    # fit quadratic a*i^2+b*i+c via 3 points then verify all
    import itertools
    pts=known[:3]
    (x1,y1),(x2,y2),(x3,y3)=pts
    # solve
    import numpy as np
    A=np.array([[x1*x1,x1,1],[x2*x2,x2,1],[x3*x3,x3,1]],float)
    Y=np.array([y1,y2,y3],float)
    try: c=np.linalg.solve(A,Y)
    except: return None
    def f(i): return c[0]*i*i+c[1]*i+c[2]
    if not all(abs(f(i)-terms[i])<1e-6 for i in range(n) if i!=b): return None
    pred=round(f(b))
    if abs(f(b)-pred)>1e-6: return None
    # describe via differences
    diffs=[terms[i+1]-terms[i] for i in range(n-1) if i!=b and i+1!=b]
    return pred, f"相鄰兩項的差會等量遞增(二階等差);依此規律,空格應為 {pred}。"

def try_fib(terms,b):
    if any(v is None for i,v in enumerate(terms) if i!=b): return None
    n=len(terms)
    if b<2: return None
    ok=all(terms[i]==terms[i-1]+terms[i-2] for i in range(2,n) if i!=b and i-1!=b and i-2!=b)
    if not ok: return None
    pred=terms[b-1]+terms[b-2]
    return pred, f"每一項等於前兩項相加;故空格 = {terms[b-2]} + {terms[b-1]} = {pred}。"

def try_interleaved(terms,b):
    n=len(terms)
    for off,label in [(0,'奇數位'),(1,'偶數位')]:
        sub_idx=list(range(off,n,2))
        sub=[terms[i] for i in sub_idx]
        if b not in sub_idx:
            # blank in the OTHER subsequence; this loop targets blank's own subsequence
            continue
        # blank position within sub
        bi=sub_idx.index(b)
        kv=[v for v in sub if v is not None]
        if len(kv)<2: return None
        # arithmetic on sub
        kidx=[j for j,v in enumerate(sub) if v is not None]
        d=sub[kidx[1]]-sub[kidx[0]]
        a0=sub[kidx[0]]-d*kidx[0]
        if all(sub[j]==a0+d*j for j in kidx):
            pred=a0+d*bi
            other='偶數位' if label=='奇數位' else '奇數位'
            return pred, f"把數列拆成兩條:第 1、3、5… 項一組,第 2、4、6… 項一組。空格所在的這條({label})是等差(每次{'+' if d>=0 else '−'}{abs(d)}),推得空格 = {pred}。"
        # geometric on sub
        if sub[kidx[0]]!=0:
            r=Fraction(sub[kidx[1]],sub[kidx[0]])
            a0g=Fraction(sub[kidx[0]])/(r**kidx[0])
            if all(Fraction(sub[j])==a0g*(r**j) for j in kidx):
                pred=a0g*(r**bi)
                if pred.denominator==1:
                    return int(pred), f"把數列拆成兩條交錯子列;空格所在這條是等比(每次×{r}),推得空格 = {int(pred)}。"
    return None

SOLVERS=[try_arith,try_geom,try_fib,try_2nd,try_interleaved]

results={}; solved=0; unsolved=[]
for q in seq:
    terms,b=parse_terms(q['stem'])
    ans_txt=q['options'].get(q['answer'],'').strip().strip('。')
    try: ans_val=int(ans_txt)
    except: ans_val=None
    got=None
    if terms is not None and ans_val is not None:
        for fn in SOLVERS:
            try: r=fn(list(terms),b)
            except Exception: r=None
            if r and r[0]==ans_val:
                got=r[1]; break
    if got:
        results[q['num']]=got; solved+=1
    else:
        unsolved.append((q['num'],q['answer'],q['stem'][:40]))

print('數列 solved %d / %d'%(solved,len(seq)))
print('unsolved:')
for u in unsolved: print('  ',u)
json.dump(results, open('/sessions/upbeat-clever-darwin/mnt/outputs/seq_exp.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
