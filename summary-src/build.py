import json, glob, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
VERSION = sys.argv[1] if len(sys.argv) > 1 else 'v44'
DATE = sys.argv[2] if len(sys.argv) > 2 else '2026-11-09'
DEST = sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, 'summary.html')

meta = json.load(open(os.path.join(HERE, 'meta.json'), encoding='utf-8'))
STEPS = json.load(open(os.path.join(HERE, 'steps.json'), encoding='utf-8'))
topics = []
for num in sorted(meta):
    m = meta[num]
    cat, _, name = m['title'].partition('－')
    if not name:
        cat, name = {'36': '神經痛', '37': '落枕', '38': '肩頸凝', '39': '便秘', '40': '失眠'}.get(num, ''), m['title']
    p = os.path.join(HERE, 'out', num + '.json')
    d = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}
    st = STEPS.get(num, {})
    d['stepsMain'] = st.get('teacher') or st.get('spec') or []
    d['stepsMainSrc'] = '重' if st.get('teacher') else '規'
    d['stepsSpec'] = st.get('spec') if st.get('teacher') else None
    p3 = os.path.join(HERE, 'out3', num + '.json')
    d['pet'] = json.load(open(p3, encoding='utf-8')) if os.path.exists(p3) else None
    d.update({'num': num, 'cat': cat, 'name': name, 'acu': m['spec_acu'], 'steps': m['spec_steps'],
              'hasTeacher': m['has_teacher']})
    topics.append(d)

GEN = json.load(open(os.path.join(HERE, 'general.json'), encoding='utf-8'))
data = json.dumps({'topics': topics, 'general': GEN}, ensure_ascii=False).replace('</', '<\\/')
tpl = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
out = tpl.replace('__DATA__', data).replace('__VERSION__', VERSION).replace('__DATE__', DATE)
open(DEST, 'w', encoding='utf-8', newline='\n').write(out)
print('wrote', DEST, len(out), 'bytes,', sum(1 for t in topics if 'etiology' in t), 'topics with data')
