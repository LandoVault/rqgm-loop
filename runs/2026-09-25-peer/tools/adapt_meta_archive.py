"""Format adapter: the meta-run workflow emitted v3 records with a few schema deviations.
Fixes FORMAT only (never decisions): setup.done -> {criteria}, add v0 version + setup check + rung record,
gates.verifier -> [] when the gate had no claims. Clock fields (budget.minutes, round.t0/t1) stay null:
the Workflow engine has no clock, and the prose forbids estimating times."""
import json, sys
src, dst = sys.argv[1], sys.argv[2]
recs = [json.loads(l) for l in open(src, encoding='utf-8') if l.strip()]
out = []
for r in recs:
    if r['t'] == 'setup':
        crit = [{'id': c['id'], 'required': True, 'kind': 'command' if c['kind'] == 'mechanical' else 'judges', **({'guardrail': True} if c.get('protected') else {})} for c in r['done']]
        out.append({'t': 'setup', 'loop': 'v3', 'done': {'criteria': crit, 'must_not_change': []}, 'models': {'generator': 'claude-opus-5-5', 'judges': ['claude-opus-5-5'] * 3},
                    'budget': {'rounds': r['budget']['rounds'], 'minutes': None, 'tokens': None}, 'final_rung': 'E2', 'note': r.get('start_rung')})
        v0 = r['best']
        out.append({'t': 'version', 'id': v0, 'parent': None, 'round': 0, 'diff': [], 'words': sum(r['words'].values())})
        out.append({'t': 'check', 'version': v0, 'rung': 'E2', 'trigger': 'setup', 'results': {c['id']: {'kind': 'command', 'value': 'pass'} for c in crit if c['kind'] == 'command'}})
        out.append({'t': 'rung', 'name': 'E2', 'by': 'human', 'note': 'start rung set by the orchestrator under the user autonomy instruction'})
        continue
    if r['t'] == 'round':
        for v in r.get('variants', []):
            g = v.setdefault('gates', {})
            if 'verifier' not in g and g.get('apply') == 'ok':
                g['verifier'] = []
    if r['t'] == 'version':
        r['words'] = sum(r['words'].values()) if isinstance(r.get('words'), dict) else r.get('words')
    out.append(r)
with open(dst, 'w', encoding='utf-8', newline='\n') as f:
    for r in out:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')
print(len(recs), '->', len(out), 'records')
