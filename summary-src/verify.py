import json, glob, re, sys
sys.stdout.reconfigure(encoding='utf-8')
def norm(s):
    return re.sub(r'[\s，,、。．.；;：:（）()「」/／]', '', s)
TOP = json.load(open('topics.json', encoding='utf-8'))
bad = 0
total = 0
for f in sorted(glob.glob('out/*.json')):
    n = f[-7:-5]
    d = json.load(open(f, encoding='utf-8'))
    src = norm(open(f'src/{n}.txt', encoding='utf-8').read()) + norm(json.dumps(TOP.get(n, {}), ensure_ascii=False))
    ms = []
    for e in d.get('etiology') or []:
        ms.append(('病因', e.get('mnemonic')))
    for k in ('timing', 'symptoms', 'anatomy'):
        o = d.get(k)
        if o and o.get('mnemonic'):
            ms.append((k, o['mnemonic']))
    for x in d.get('extra_sections') or []:
        if x.get('mnemonic'):
            ms.append(('extra', x['mnemonic']))
    for k, m in ms:
        if not m:
            continue
        total += 1
        parts = re.split(r'或|／|/', m)
        for p in parts:
            p = norm(p)
            if p and p not in src:
                bad += 1
                print(n, k, '原文找不到：', m, '→', p)
print('checked', total, 'mnemonics, problems', bad)
