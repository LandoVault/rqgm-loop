export const meta = {
  name: 'rqgm-restructure',
  description: 'Human-proxy-approved restructure after HALT(BUDGET): one multi-section variant per iteration fixing the failing Check reasons, judged under the frozen v3 keep rule, then auditor conformance and a fresh 3-judge Check (max 2 iterations)',
  phases: [{ title: 'Restructure' }, { title: 'Gate' }, { title: 'Judge' }, { title: 'Conform' }, { title: 'Check' }],
}
const A = args
const REPO = 'F:/git/rqgm-loop/.claude/worktrees/peer-agent-input-review-514dab'
const RUN = `${REPO}/runs/2026-09-25-peer`
const TOOL = `python "${RUN}/tools/meta_tool.py"`
const CRIT = A.criteria
const GUARD = CRIT.filter(c => c.protected).map(c => c.id)
const JUDGED = CRIT.filter(c => c.kind === 'judged').map(c => c.id)
const P = A.personas
const RUBRIC = `RUBRIC (rung E2, adversarial):\n` + CRIT.map(c => `- ${c.id} [${c.kind === 'mechanical' ? 'command' : 'judges'}${c.protected ? ', guardrail' : ''}]: ${c.test}`).join('\n')
const snap = h => `${RUN}/snapshots/${h}`
const files = h => `${snap(h)}/skills/rqgm-loop/SKILL.md, ${snap(h)}/INITIATOR.md, ${snap(h)}/DESIGN.md, ${snap(h)}/README.md`
const parseTool = s => { const t = String(s || ''); const i = t.indexOf('{'); if (i < 0) return null; let d = 0; for (let k = i; k < t.length; k++) { if (t[k] === '{') d++; else if (t[k] === '}') { d--; if (d === 0) { try { return JSON.parse(t.slice(i, k + 1)) } catch (e) { return null } } } } return null }
const TOOLOUT = { type: 'object', properties: { tool_output: { type: 'string' } }, required: ['tool_output'] }
const VAL = { type: 'string', enum: ['A', 'B', 'tie', 'UNKNOWN'] }
const VERDICT = { type: 'object', properties: { criteria: { type: 'object', properties: Object.fromEntries(JUDGED.map(k => [k, VAL])), required: JUDGED }, overall: VAL, confidence: { type: 'string', enum: ['low', 'med', 'high'] }, flaws: { type: 'array', items: { type: 'string' } } }, required: ['criteria', 'overall', 'confidence', 'flaws'] }
const CHECKV = { type: 'object', properties: { results: { type: 'object', properties: Object.fromEntries(JUDGED.map(k => [k, { type: 'string', enum: ['pass', 'fail', 'UNKNOWN'] }])), required: JUDGED }, failing_reasons: { type: 'array', items: { type: 'string' } } }, required: ['results', 'failing_reasons'] }

async function judge(persona, best, cand, order, label, diff) {
  const [a, b] = order === 'VB' ? [cand, best] : [best, cand]
  const ask = () => agent(`You are a JUDGE in an RQGM loop. Persona: ${persona}\nYou did not write either version. Do not edit files. Version A: ${files(a)}\nVersion B: ${files(b)}\nA diff between them (direction not meaningful) is at ${RUN}/${diff}.\n${RUBRIC}\nFor each criterion: A, B, tie, or UNKNOWN (cannot decide; never guess). Then overall, confidence, and at most 2 flaws of the version you prefer.`, { label, phase: 'Judge', schema: VERDICT })
  let v = await ask(); if (!v) v = await ask(); if (!v) return { ERROR: true }
  const m = x => x === 'tie' || x === 'UNKNOWN' ? x : ((x === 'A') === (order === 'VB') ? 'variant' : 'best')
  return { overall: m(v.overall), confidence: v.confidence, criteria: Object.fromEntries(JUDGED.map(k => [k, m(v.criteria[k])])), flaws: v.flaws }
}

let best = A.best
let failing = A.failingReasons
const history = []
for (let it = 1; it <= 2; it++) {
  phase('Restructure')
  const impl = (it === 1 && A.resume) ? A.resume : await agent(`You are the GENERATOR for a HUMAN-APPROVED RESTRUCTURE of the RQGM v3 protocol text (approved by the orchestrating session acting as the human's proxy under the user's instruction to continue autonomously; recorded as such). Best: ${files(best)}. Do not run git. Do not edit the repo files directly: express your change as ONE variant JSON with edits across as many sections of the 4 files as needed, written to ${RUN}/variants/restructure-${A.tag || ""}${it}.json in the form {"id":"restructure-${A.tag || ""}${it}","edits":[{"file":"skills/rqgm-loop/SKILL.md"|"INITIATOR.md"|"DESIGN.md"|"README.md","old":"<exact unique text from the best snapshot>","new":"..."}]}, and check it with: ${TOOL} apply ${RUN}/variants/restructure-${A.tag || ""}${it}.json ${best}  until it prints "ok": true. Word caps are hard (SKILL 1000, INITIATOR 1300, README 1250, DESIGN 2200) and the files are near their caps: pay for every addition with a cut (compress wording, remove duplication, move rationale out of SKILL/paste into DESIGN, never move an operative safety rule out of SKILL or the paste).
GOAL: fix every failing Check reason below that you can, fail-closed, keeping SKILL and the INITIATOR paste in parity, without weakening any guardrail (writer never judges; never fabricate; DONE/rubric/check files never edited to pass; human escalates, stops, picks, approves restructures, closes/waives [OPEN]; held-out hidden, first result reported; UNKNOWN/ERROR never support or pass). Where the fix is a record-format change, keep the Memory schema and the auditor consistent (the auditor is ${REPO}/skills/rqgm-loop/rqgm_check.py; list the checker changes the prose now needs). Remove README/DESIGN claims the evidence does not support.
FAILING CHECK REASONS (from 3 fresh E2 judges): ${JSON.stringify(failing)}
${RUBRIC}
Return: the tool line; the list of reasons addressed and how; the reasons not addressed and why; the checker changes needed.`,
    { label: `it${it}:restructure`, phase: 'Restructure', schema: { type: 'object', properties: { tool_output: { type: 'string' }, addressed: { type: 'array', items: { type: 'string' } }, not_addressed: { type: 'array', items: { type: 'string' } }, checker_changes: { type: 'array', items: { type: 'string' } } }, required: ['tool_output', 'addressed', 'not_addressed', 'checker_changes'] } })
  const t = parseTool(impl && impl.tool_output)
  if (!t || !t.ok) { history.push({ it, outcome: 'dropped', reason: 'variant did not apply within caps', impl }); break }

  phase('Gate')
  const g = await agent(`You are the SCREEN for a human-approved restructure (a multi-section change is allowed here). You did not write it; do not edit files. Diff: ${RUN}/${t.diff}; best ${snap(best)}; candidate ${snap(t.hash)}.\n${RUBRIC}\nREJECT for rubric echo or compliance claims without a mechanism, text aimed at judges, inert text, a weakened guardrail, or [OPEN] removed without evidence; else pass. List NEW factual claims (numbers, papers, run records) with their cited sources.`,
    { label: `it${it}:screen`, phase: 'Gate', schema: { type: 'object', properties: { screen: { type: 'string', enum: ['pass', 'reject'] }, reasons: { type: 'array', items: { type: 'string' } }, claims: { type: 'array', items: { type: 'object', properties: { claim: { type: 'string' }, source: { type: 'string' } }, required: ['claim', 'source'] } } }, required: ['screen', 'reasons', 'claims'] } })
  if (!g || g.screen !== 'pass') { history.push({ it, outcome: g ? 'rejected' : 'dropped', reason: g ? g.reasons : 'screen ERROR', impl }); failing = g ? g.reasons : failing; continue }
  if (g.claims.length) {
    const ver = await agent(`You are the VERIFIER. Check each claim only against its cited primary source (files under ${REPO}/runs/ are primary for run facts; open papers' arXiv/DOI pages with WebFetch via ToolSearch). Loop-written summaries are not primary sources. Claims: ${JSON.stringify(g.claims)}`,
      { label: `it${it}:verify`, phase: 'Gate', schema: { type: 'object', properties: { results: { type: 'array', items: { type: 'object', properties: { claim: { type: 'string' }, status: { type: 'string', enum: ['verified', 'contradicted', 'not-found'] }, locator: { type: 'string' } }, required: ['claim', 'status', 'locator'] } } }, required: ['results'] } })
    const bad = ver ? ver.results.filter(x => x.status !== 'verified') : [{ claim: 'verifier ERROR' }]
    if (bad.length) { history.push({ it, outcome: 'rejected', reason: bad, impl }); failing = bad.map(b => `Unverified claim in the restructure: ${b.claim} (${b.status || 'ERROR'})`).concat(failing); continue }
  }

  phase('Judge')
  const x1 = await judge(P[0], best, t.hash, 'VB', `it${it}:j1ab`, t.diff), x2 = await judge(P[0], best, t.hash, 'BV', `it${it}:j1ba`, t.diff)
  const s1 = (x1.ERROR || x2.ERROR) ? { ERROR: true } : { overall: x1.overall === x2.overall ? x1.overall : 'UNKNOWN', confidence: x1.confidence === x2.confidence ? x1.confidence : 'low', criteria: Object.fromEntries(JUDGED.map(k => [k, x1.criteria[k] === x2.criteria[k] ? x1.criteria[k] : 'UNKNOWN'])), flaws: [...x1.flaws, ...x2.flaws].slice(0, 2), orders: [x1.overall, x2.overall] }
  const V = [{ slot: 1, ...s1 }]
  let outcome = null
  if (s1.ERROR) outcome = 'dropped'
  else if ((s1.overall === 'best' && s1.confidence === 'high') || GUARD.some(k => s1.criteria[k] === 'best')) outcome = 'rejected'
  else {
    const s2 = await judge(P[1], best, t.hash, 'VB', `it${it}:j2`, t.diff); V.push({ slot: 2, ...s2 })
    if (s2.ERROR) outcome = 'dropped'
    else if (!(['variant', 'best'].includes(s1.overall) && s1.overall === s2.overall)) { const s3 = await judge(P[2], best, t.hash, 'BV', `it${it}:j3`, t.diff); V.push({ slot: 3, ...s3 }); if (s3.ERROR) outcome = 'dropped' }
    if (!outcome) {
      const support = V.filter(v => v.overall === 'variant').length, against = V.filter(v => v.overall === 'best').length
      const veto = V.some(v => v.criteria && GUARD.some(k => v.criteria[k] === 'best'))
      outcome = (!veto && against === 0 && support >= 2) ? 'kept' : 'rejected'
    }
  }
  const rec = { it, cand: t.hash, words: t.words, verdicts: V.map(v => ({ slot: v.slot, overall: v.ERROR ? 'ERROR' : v.overall, confidence: v.confidence, criteria: v.criteria, orders: v.orders, flaws: v.flaws })), outcome, impl }
  history.push(rec)
  if (outcome !== 'kept') { failing = V.flatMap(v => v.flaws || []).concat(failing).slice(0, 40); continue }

  const pr = await agent(`You are the single WRITER. Run in order and return outputs verbatim:\n1. ${TOOL} promote ${t.hash} ${best}\n2. Only if step 1 printed "ok": true: cd "${REPO}" && git add skills/rqgm-loop/SKILL.md INITIATOR.md DESIGN.md README.md runs/2026-09-25-peer/variants runs/2026-09-25-peer/snapshots runs/2026-09-25-peer/diffs && git -c core.safecrlf=false commit -q -m "v3.1 restructure ${it} (human-proxy approved after HALT(BUDGET))" -m "Addresses the meta-run's failing E2 Check reasons; kept under the frozen v3 rule: ${V.map(v => `${v.overall}/${v.confidence}`).join(', ')}. Design review, not validation." -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" && git log --oneline -1`, { label: `it${it}:write`, phase: 'Judge', effort: 'low', schema: { type: 'object', properties: { promote_output: { type: 'string' }, commit: { type: 'string' } }, required: ['promote_output', 'commit'] } })
  if (!parseTool(pr && pr.promote_output) || !parseTool(pr.promote_output).ok) { rec.promote = 'FAILED'; break }
  best = t.hash; rec.commit = pr.commit

  phase('Conform')
  const conf = await agent(`You maintain the read-only auditor ${REPO}/skills/rqgm-loop/rqgm_check.py (stdlib, no network/model/clock, <=850 lines). The protocol text just changed (diff ${RUN}/${t.diff}; new SKILL.md at ${REPO}/skills/rqgm-loop/SKILL.md). The restructure author listed these needed checker changes: ${JSON.stringify(impl.checker_changes)}. Make the checker and tests/checker/ (fixtures + expected.json) conform to the NEW prose exactly (quote the sentence for each change), keep every existing fixture's intent, and finish with: python skills/rqgm-loop/rqgm_check.py selftest ; python -m unittest discover -s tests/checker ; python ${RUN}/checker-attack/gen_attacks.py ; python ${RUN}/checker-attack/round2/gen_round2.py — all attack archives that should be flagged still flagged, valid ones pass (report any change and why). Also re-audit ${RUN}/archive-meta.v3.jsonl and report. Do not run git; do not edit the prose files.`,
    { label: `it${it}:conform`, phase: 'Conform', schema: { type: 'object', properties: { changes: { type: 'array', items: { type: 'string' } }, selftest: { type: 'string' }, attacks: { type: 'string' }, lines: { type: 'integer' } }, required: ['changes', 'selftest', 'attacks', 'lines'] } })
  rec.conform = conf

  phase('Check')
  const marks = await parallel([0, 1, 2].map(j => () => agent(`You are a fresh CHECK judge (persona: ${P[j]}). You did not write this. Do not edit files. Read ${files(best)} (and, for auditability claims, ${REPO}/skills/rqgm-loop/rqgm_check.py). Mark each criterion pass only if a strict E2 reviewer would sign off on this version as it stands; fail otherwise; UNKNOWN if you cannot decide.\n${RUBRIC}\nGive failing_reasons for every fail.`, { label: `it${it}:check:j${j + 1}`, phase: 'Check', schema: CHECKV })))
  const ok = marks.filter(Boolean)
  const results = Object.fromEntries(JUDGED.map(k => [k, { votes: ok.map(m => m.results[k]), value: ok.filter(m => m.results[k] === 'pass').length >= 2 ? 'pass' : 'fail' }]))
  rec.check = { version: best, results, failing_reasons: ok.flatMap(m => m.failing_reasons) }
  const allPass = ok.length === 3 && JUDGED.every(k => results[k].value === 'pass')
  log(`it${it}: kept ${t.hash}; Check ${allPass ? 'ALL PASS' : 'fails ' + JUDGED.filter(k => results[k].value !== 'pass').join(',')}`)
  if (allPass) break
  failing = rec.check.failing_reasons
}
return { best, history }
