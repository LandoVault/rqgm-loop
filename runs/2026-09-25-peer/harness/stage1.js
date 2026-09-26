export const meta = {
  name: 'rqgm-stage1-decisions',
  description: 'Stage 1: 30 frozen decision scenarios; answer key from rqgm_check.py --pending, adjudicated against the prose; 3 fresh contexts per scenario answer from SKILL.md alone; deterministic scoring per rule class',
  phases: [
    { title: 'Author', detail: '30 scenarios + keys from the auditor' },
    { title: 'Adjudicate', detail: 'independent prose reading of every key' },
    { title: 'Answer', detail: '3 fresh contexts x 30 scenarios, SKILL.md only' },
  ],
}
const REPO = 'F:/git/rqgm-loop/.claude/worktrees/peer-agent-input-review-514dab'
const S1 = `${REPO}/runs/2026-09-25-peer/stage1`
const SKILL = args.skill           // path of the frozen SKILL.md the answerers read (a copy outside the repo's tests)
const CLASSES = [
  'ERROR vs tie (a failed/unparsable judge result)', 'judge-1 order disagreement (UNKNOWN)', 'judge-3 trigger (incl. UNKNOWN/UNKNOWN and tie/tie on a shorter variant)',
  'strict-mode keep (3/3)', 'strict-mode Check (3/3)', 'pruning on ties needs a full clean panel', 'protected-item veto', 'command regression vs a failure best shares',
  'selection tie-break (most support, then shorter, then first)', 'all-ERROR rounds and HALT(ERROR)', 'stall count and when a Check is due',
  'standing Check / held-out result reuse until best, rung or DONE changes', 'held-out fail -> reruns, spare gating, HALT(OVERFIT)/HALT(STALL)',
  'budget start rule and HALT(BUDGET)', 'amend and E3; required vs optional [OPEN]; torn-line resume; escalation probe and stall reset',
]
const ANSWER = { type: 'object', properties: {
  outcomes: { type: 'object', description: 'variant id -> kept | rejected | dropped | pending (pending = more judge results are required before deciding)' },
  judge_needed: { type: 'string', description: 'the next judge slot that must run for a pending variant ("1","2","3") or "none"' },
  next: { type: 'string', enum: ['next_round', 'run_judges', 'check', 'boundary', 'held_out', 'HALT(STALL)', 'HALT(OPEN)', 'HALT(ERROR)', 'HALT(BUDGET)', 'HALT(OVERFIT)', 'HALT(OSCILLATION)', 'COMPLETE', 'PARTIAL'] },
  strict: { type: 'boolean', description: 'is strict mode in force for this round' },
  why: { type: 'string' } }, required: ['outcomes', 'judge_needed', 'next', 'strict', 'why'] }

phase('Author')
const authored = await agent(`You are the SCENARIO AUTHOR for a pre-registered test of whether LLM orchestrators apply the RQGM v3 prose correctly. Do NOT run git; write only under ${S1}/.
Read ${SKILL} (the frozen SKILL.md; it is the contract), ${REPO}/skills/rqgm-loop/rqgm_check.py (the read-only auditor; see its --pending option) and ${REPO}/tests/checker/fixtures/ (archive examples in the exact v3 record format).
Write exactly 30 scenarios, 2 per rule class below, as ${S1}/scenarios/sNN/archive.jsonl (a valid v3 MEMORY up to the start of the decision) + ${S1}/scenarios/sNN/pending.json (the new results for the current round: gates and judge verdicts as the Memory schema defines them) + ${S1}/scenarios/sNN/question.md (one short paragraph stating what has just happened, in plain words, with no hint of the answer). Vary surface details; make half of the scenarios ones where a careless reading gives the wrong answer.
For each, derive the expected decision with the auditor (run rqgm_check.py audit ${S1}/scenarios/sNN/archive.jsonl --pending ${S1}/scenarios/sNN/pending.json and read its output) and write ${S1}/keys/sNN.json in exactly this schema: ${JSON.stringify(ANSWER.properties)} (fill "why" with the SKILL.md sentences that decide it). If the auditor cannot decide a field, derive it from the SKILL.md text yourself and mark "why" with "KEY-FROM-PROSE".
Rule classes: ${CLASSES.map((c, i) => `${i + 1}. ${c}`).join(' | ')}
Also write ${S1}/index.json: [{id, class, careless_trap: true|false}]. Return a one-paragraph summary.`, { label: 'author', phase: 'Author' })

phase('Adjudicate')
const ADJ = { type: 'object', properties: { items: { type: 'array', items: { type: 'object', properties: {
  id: { type: 'string' }, agree: { type: 'boolean' }, prose_answer: ANSWER, note: { type: 'string' } }, required: ['id', 'agree', 'prose_answer', 'note'] } } }, required: ['items'] }
const adj = await agent(`You are the ADJUDICATOR (standing in for the human, who must adjudicate the answer key against the prose before scoring). For each scenario under ${S1}/scenarios/ (read index.json), read archive.jsonl, pending.json and question.md, then decide the answer yourself from ${SKILL} ALONE (do not read the keys or the auditor first). Then read ${S1}/keys/sNN.json and say whether it agrees with your reading on every field; where it does not, explain which is right by quoting SKILL.md. Do not edit files.`,
  { label: 'adjudicate', phase: 'Adjudicate', schema: ADJ })

phase('Answer')
const ids = Array.from({ length: 30 }, (_, i) => `s${String(i + 1).padStart(2, '0')}`)
const answers = await parallel(ids.flatMap(id => [1, 2, 3].map(c => () => agent(`You are the ORCHESTRATOR of an RQGM loop, in a fresh context (${id}, context ${c}). The protocol is ONLY the file ${SKILL}; read it fully and apply it exactly as written. Do not read any other file except these three: ${S1}/scenarios/${id}/archive.jsonl (your MEMORY so far), ${S1}/scenarios/${id}/pending.json (the new results for the current round), ${S1}/scenarios/${id}/question.md. Decide what the protocol requires now.`,
  { label: `${id}:c${c}`, phase: 'Answer', schema: ANSWER }).then(a => ({ id, c, a })))))
return { authored, adjudication: adj, answers: answers.filter(Boolean) }
