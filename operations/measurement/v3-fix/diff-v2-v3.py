import difflib, sys

v2 = open('operations/measurement/v3-fix/gtm-v2.js').read()
v3 = open('operations/measurement/v3-fix/gtm-v3.js').read()
print('identical:', v2 == v3, '| v2 len:', len(v2), '| v3 len:', len(v3))
if v2 == v3:
    sys.exit(0)

# token-level diff on a coarse split to keep it fast
def toks(s):
    # split into identifiers/strings/numbers/punct
    import re
    return re.findall(r'"[^"]*"|[A-Za-z_$][A-Za-z0-9_$]*|\d+|\S', s)

t2, t3 = toks(v2), toks(v3)
sm = difflib.SequenceMatcher(None, t2, t3, autojunk=True)
print('token similarity: %.6f' % sm.ratio())
n = 0
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        continue
    n += 1
    if n <= 30:
        left = ' '.join(t2[i1:i2])[:220]
        right = ' '.join(t3[j1:j2])[:220]
        print(f'--- {tag}:')
        print(f'    v2: {left}')
        print(f'    v3: {right}')
print('total diff hunks:', n)
