import re, json, html, sys
src = sys.argv[1]
s = open(src, encoding='utf-8').read()
BS = chr(92)
out = {}
for m in re.finditer(r'<div class="ver-panel[^"]*" id="vp-(\d\d)-(\w+)"', s):
    out.setdefault(m.group(1), {})[m.group(2)] = m.start()
titles = dict(re.findall(r'id="topic-(\d\d)"[\s\S]{0,600}?<h2 class="topic-title">([^<]+)</h2>', s))
res = {}
starts = sorted([(p, t, v) for t, d in out.items() for v, p in d.items()])
STR = "'((?:[^'" + BS + BS + "]|" + BS + BS + ".)*)'"
mn_re = re.compile(r"showMnem\(" + STR + "," + STR + r"\)")
def unesc(x):
    return x.replace(BS + 'n', '\n').replace(BS + "'", "'")
for i, (p, t, v) in enumerate(starts):
    end = starts[i + 1][0] if i + 1 < len(starts) else len(s)
    chunk = s[p:end]
    secs = []
    parts = re.split(r'<span class="sec-label"[^>]*>', chunk)
    for part in parts[1:]:
        label = part.split('</span>')[0]
        body = part.split('</span>', 2)[-1]
        acus = re.findall(r'class="acu-tag[^"]*"[^>]*>([^<]+)<', body)
        mn = mn_re.findall(body)
        txt = re.sub(r'<button class="acu-tag[\s\S]*?</button>', '', body)
        txt = re.sub(r'</(p|div|li)>', '\n', txt)
        txt = re.sub(r'<[^>]+>', '', txt)
        txt = html.unescape(txt).strip()
        secs.append({'label': label, 'acus': acus,
                     'mnem_popups': [(unesc(a), unesc(b)) for a, b in mn], 'text': txt})
    res.setdefault(t, {'title': titles.get(t, '')})[v] = secs
json.dump(res, open('topics.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
with open('summary.txt', 'w', encoding='utf-8') as f:
    for t in sorted(res):
        vs = {v: [sec['label'] for sec in x] for v, x in res[t].items() if v != 'title'}
        nm = sum(len(sec['mnem_popups']) for v, x in res[t].items() if v != 'title' for sec in x)
        f.write(f"{t} {res[t]['title']} mnem_popups={nm}\n")
        for v, labs in vs.items():
            f.write(f"   {v}: {' '.join(labs)}\n")
