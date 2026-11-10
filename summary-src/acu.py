"""從 index.html 抽出每題穴位：重點整理版優先，其次規範版（穴名、分組說明、定位）。輸出 acu.json。"""
import re, json, sys, html, os
HERE = os.path.dirname(os.path.abspath(__file__))
s = open(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'index.html'), encoding='utf-8').read()
BS = chr(92)
STR = "'((?:[^'" + BS + BS + "]|" + BS + BS + ".)*)'"
acu_re = re.compile(r"<button class=\"acu-tag[^\"]*\"[^>]*onclick=\"showAcu\(" + STR + "," + STR + r"\)\"[^>]*>([^<]+)</button>|<button class=\"acu-tag[^\"]*\"[^>]*>([^<]+)</button>")
def unesc(x):
    return x.replace(BS + 'n', '\n').replace(BS + "'", "'")
def clean_loc(t):
    t = unesc(t)
    t = re.sub(r'\n*【來源：[^】]*】', '', t)
    return re.sub(r'\s+', ' ', t).strip()
out = {}
for num in ['%02d' % i for i in range(1, 41)]:
    res = None
    for ver in ('teacher', 'spec'):
        m = re.search(r'id="sb-' + num + '-' + ver + r'-acu">', s)
        if not m:
            continue
        body = s[m.end():m.end() + 40000]
        body = body[:body.find('<div class="sec-wrap"')] if '<div class="sec-wrap"' in body else body
        summ = re.search(r'class="acu-summary">(.*?)</p>', body)
        summary = html.unescape(re.sub(r'<[^>]+>', '', summ.group(1))).strip() if summ else ''
        # 依段落切出分組（例如三叉神經分支、口訣組）
        groups = []
        cur = {'label': '', 'pts': []}
        for tok in re.finditer(r'第\d組口訣：[^<]+|<p class="acu-group[^"]*">([^<]+)</p>|<h4[^>]*>([^<]+)</h4>|' + acu_re.pattern, body):
            g = tok.group(0)
            if g.startswith('第') or g.startswith('<p') or g.startswith('<h4'):
                if cur['pts']:
                    groups.append(cur)
                lab = tok.group(1) or tok.group(2) or g
                cur = {'label': html.unescape(lab).strip(), 'pts': []}
            else:
                name = (tok.group(5) or tok.group(6) or '').strip()
                loc = clean_loc(tok.group(4)) if tok.group(4) is not None else ''
                cur['pts'].append({'n': name, 'loc': loc})
        if cur['pts']:
            groups.append(cur)
        notes = [html.unescape(re.sub(r'<[^>]+>', '', x)).strip() for x in re.findall(r'<p(?: class="(?!acu-summary)[^"]*")?>(.*?)</p>', body)]
        notes = [x for x in notes if x and not x.startswith('共 ') and not re.match(r'^共\d+個?$', x)]
        if groups:
            res = {'ver': ver, 'summary': summary, 'groups': groups, 'notes': notes}
            cnt = re.search(r'(\d+)', summary)
            total = sum(len(g['pts']) for g in groups)
            if cnt and int(cnt.group(1)) != total:
                res['mismatch'] = ('寫共 %s 穴，不重複穴名 %d 個（分體位時有重複按的穴）' if notes else '寫共 %s 穴，實列 %d 穴') % (cnt.group(1), total)
            break
    out[num] = res
json.dump(out, open(os.path.join(HERE, 'acu.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
sys.stdout.reconfigure(encoding='utf-8')
for n, r in out.items():
    print(n, r['ver'], r['summary'], [(g['label'][:12], len(g['pts'])) for g in r['groups']], sum(len(g['pts']) for g in r['groups']))
