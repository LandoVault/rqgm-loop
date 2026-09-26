export const meta = {
  name: 'rqgm-pilot-run',
  description: 'One pilot run (arm x task): V/P = orchestrator-in-the-loop relay of a frozen protocol; S = single strong agent; B = best-of-N with the same checks. The harness decides nothing; it relays, journals, runs the sealed human proxy and caps calls.',
  phases: [{ title: 'Run' }, { title: 'Proxy', detail: 'sealed human-proxy decisions and held-out judges' }],
}

// args: {runId, arm: 'V'|'P'|'S'|'B', task, ws, protocol: [paths] (V/P), cap, heldout: [3 prompts], spares: [3 prompts], doneText, criteria: [ids]}
const A = args
const WS = A.ws
const CAP = A.cap
const journal = []
let calls = 0              // model calls charged to the arm (orchestrator steps + roles); proxy calls counted separately
let proxyCalls = 0
const J = e => { journal.push(e); return e }

const PREAMBLE = (role, id) => `You are a SUBAGENT in a controlled study run (${A.runId}). Role requested by the orchestrator: ${role}. Request id: ${id}.
Workspace: ${WS}. You may READ any file in the workspace. Do NOT modify ${WS}/archive.jsonl or the task's target/check files; if you need scratch files (e.g. extra tests, a candidate copy), create them only under ${WS}/scratch/${id}/. Do not read anything outside the workspace. Return your answer as text exactly in the format the orchestrator asks for.
--- orchestrator's request follows ---
`

const ORCH = { type: 'object', properties: {
  did: { type: 'string', description: 'what you did yourself this step (files written, commands run, records appended), briefly' },
  requests: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, role: { type: 'string' }, prompt: { type: 'string', description: 'complete, self-contained instructions for a fresh subagent' } }, required: ['id', 'role', 'prompt'] } },
  human: { type: 'object', properties: { kind: { type: 'string', enum: ['none', 'escalate', 'heldout', 'heldout_spare', 'oscillation_pick', 'confirm_done', 'other'] }, text: { type: 'string' } }, required: ['kind', 'text'] },
  finished: { type: 'object', properties: { yes: { type: 'boolean' }, status: { type: 'string', description: 'your protocol\'s final status/exit (e.g. COMPLETE, PARTIAL, HALT(STALL), DONE)' }, claims_done: { type: 'boolean', description: 'true if you claim the target now meets DONE' }, output: { type: 'string' } }, required: ['yes', 'status', 'claims_done', 'output'] } },
  required: ['did', 'requests', 'human', 'finished'] }

async function proxy(h) {                   // sealed human-proxy script (pilot-heldout-and-proxy.md)
  if (h.kind === 'escalate') return 'Human: yes, escalate (up to the DONE final rung).'
  if (h.kind === 'oscillation_pick') return 'Human: pick the newer version.'
  if (h.kind === 'confirm_done') return 'Human: DONE.json is confirmed as given; no amendments.'
  if (h.kind === 'heldout' || h.kind === 'heldout_spare') {
    const spare = h.kind === 'heldout_spare'
    const set = spare ? A.spares : A.heldout
    const marks = await parallel(set.map((p, i) => () => { proxyCalls++; return agent(`You are a held-out FINAL judge for a controlled study (${A.runId}). ${p}
Task workspace (read only; do not modify anything; scratch space: ${WS}/scratch/heldout-${journal.length}-${i}/): ${WS}. DONE criteria (from ${WS}/DONE.json):\n${A.doneText}
Mark each criterion pass or fail for the target as it stands now (for command criteria, run the command yourself in a scratch copy).`,
      { label: `proxy:heldout:${i + 1}`, phase: 'Proxy', schema: { type: 'object', properties: Object.fromEntries(A.criteria.map(k => [k, { type: 'string', enum: ['pass', 'fail'] }])), required: A.criteria } }) }))
    const ok = marks.filter(Boolean).map(m => ({ results: m }))
    const ids = A.criteria
    const failing = ids.filter(k => ok.filter(m => m.results[k] === 'pass').length < 2)
    J({ t: 'heldout', set: spare ? 'spares' : 'primary', marks: ok.map(m => m.results), failing })
    return `Human: held-out check done (${spare ? 'spare' : 'primary'} set, majority per criterion). Failing criterion IDs: ${failing.length ? failing.join(', ') : 'none'}.`
  }
  return 'Human: no decision; proceed per your protocol.'
}

let final = null
phase('Run')
if (A.arm === 'V' || A.arm === 'P') {
  let lastResults = []
  let humanAnswer = null
  for (let step = 1; ; step++) {
    if (calls >= CAP) { J({ t: 'cap', calls }); break }
    calls++
    const o = await agent(`You are the ORCHESTRATOR of an RQGM loop in a controlled study run (${A.runId}). Follow ONLY the protocol in these files, exactly as written: ${A.protocol.join(', ')}.
Your host cannot spawn subagents directly. Instead, each time you need a role (generator, screen, verifier, judge, check judge, etc.) you emit a request; the harness runs each request in a fresh, separate subagent (a different context from you) and returns its raw output to you at your next step. Requests you emit in one step run in parallel. You yourself are the single writer: you may read/write files in the workspace, apply diffs, run commands (e.g. tests), and append records.
Workspace: ${WS}. The task's DONE is ${WS}/DONE.json; slots: TARGET and GROUNDING are described there and in the workspace files; EVALUATORS: choose per your protocol; MEMORY: ${WS}/archive.jsonl (create it if absent; it is your only memory between steps — you are re-invoked fresh every step, so record everything you need there); BUDGET: at most ${CAP} model calls in total for this run (this orchestrator step counts; ${calls} used including this one); the human is reachable only through the 'human' field.
Human decisions available: escalation, the held-out check (human.kind 'heldout' for the primary set, 'heldout_spare' for the spare set; the human runs those held-out judges and returns failing criterion IDs only), the oscillation pick, DONE confirmation. Anything else gets "no decision".
Results of the requests you emitted last step (verbatim): ${JSON.stringify(lastResults).slice(0, 60000)}
Human's answer to your last question: ${humanAnswer || 'none'}
Do the next step now. When your protocol reaches an exit, set finished.yes=true with your protocol's status and output.`,
      { label: `step${step}:orchestrator`, phase: 'Run', schema: ORCH })
    if (!o) { J({ t: 'orchestrator_error', step }); if (journal.filter(e => e.t === 'orchestrator_error').length >= 2) break; continue }
    J({ t: 'orch', step, did: o.did, requests: o.requests.map(r => ({ id: r.id, role: r.role, prompt: r.prompt })), human: o.human, finished: o.finished })
    if (o.finished && o.finished.yes) { final = { status: o.finished.status, claims_done: o.finished.claims_done, output: o.finished.output }; break }
    humanAnswer = o.human && o.human.kind !== 'none' ? await proxy(o.human) : null
    if (humanAnswer) J({ t: 'human', q: o.human, a: humanAnswer })
    const reqs = o.requests.slice(0, Math.max(0, CAP - calls))
    if (reqs.length < o.requests.length) J({ t: 'cap_truncated', dropped: o.requests.slice(reqs.length).map(r => r.id) })
    calls += reqs.length
    lastResults = await parallel(reqs.map(r => async () => {
      const out = await agent(PREAMBLE(r.role, r.id) + r.prompt, { label: `step${step}:${r.role}:${r.id}`.slice(0, 60), phase: 'Run' })
      return { id: r.id, role: r.role, output: out === null ? 'ERROR: the subagent failed or timed out' : out }
    }))
    lastResults = lastResults.map((x, i) => x || { id: reqs[i].id, role: reqs[i].role, output: 'ERROR: the subagent failed or timed out' })
    J({ t: 'results', step, results: lastResults })
  }
} else if (A.arm === 'S') {
  calls = 1
  const o = await agent(`You are working alone on a task in a controlled study run (${A.runId}). Workspace: ${WS}. Read ${WS}/DONE.json and every file in the workspace. Improve the target until every required DONE criterion holds, iterating as you see fit: diagnose, revise, run the public checks and any extra tests you write (put scratch files under ${WS}/scratch/), re-check. Never edit check files, spec files, the corpus or DONE.json. Never invent data: a value you cannot support from the workspace must be written as [OPEN: reason]. Budget: work until you are satisfied or you have done at most ${Math.max(3, Math.floor(CAP / 4))} revise-and-check cycles. Finish by reporting your status.`,
    { label: 'S:agent', phase: 'Run', schema: { type: 'object', properties: { status: { type: 'string', enum: ['DONE', 'INCOMPLETE'] }, open_items: { type: 'array', items: { type: 'string' } }, cycles: { type: 'integer' }, summary: { type: 'string' } }, required: ['status', 'open_items', 'cycles', 'summary'] } })
  J({ t: 'S', result: o })
  final = o ? { status: o.status, claims_done: o.status === 'DONE', output: o.summary } : { status: 'ERROR', claims_done: false, output: '' }
} else if (A.arm === 'B') {
  const N = Math.max(2, Math.floor(CAP / 2))
  const cands = await parallel(Array.from({ length: N }, (_, i) => async () => {
    calls++
    const r = await agent(`You are one of ${N} independent attempts in a controlled study run (${A.runId}); attempt ${i + 1}. Workspace (read only): ${WS}. Read ${WS}/DONE.json and the workspace files. Make ONE fresh revision of the target that best satisfies every required DONE criterion: copy the whole workspace to ${WS}/scratch/cand-${i + 1}/ and edit the target only there. Never edit check files, spec files, the corpus or DONE.json. Never invent data: write [OPEN: reason] for anything the workspace cannot support. Then run the public checks named in DONE.json inside your copy and report their exit status.`,
      { label: `B:cand${i + 1}`, phase: 'Run', schema: { type: 'object', properties: { dir: { type: 'string' }, public_checks_pass: { type: 'boolean' }, words: { type: 'integer' } }, required: ['dir', 'public_checks_pass', 'words'] } })
    if (!r) return null
    calls++
    const v = await agent(`You are a VERIFIER in a controlled study run (${A.runId}). Candidate: ${WS}/scratch/cand-${i + 1}/ (read only; scratch: ${WS}/scratch/ver-${i + 1}/). Check every DONE criterion of kind "source" in ${WS}/DONE.json against the workspace's sources (spec.md or corpus/), writing and running extra tests in scratch if useful. Return the number of criteria you find violated and short reasons.`,
      { label: `B:verify${i + 1}`, phase: 'Run', schema: { type: 'object', properties: { flags: { type: 'integer' }, reasons: { type: 'array', items: { type: 'string' } } }, required: ['flags', 'reasons'] } })
    return { i: i + 1, ...r, flags: v ? v.flags : 99, reasons: v ? v.reasons : ['verifier ERROR'] }
  }))
  const ok = cands.filter(Boolean).sort((a, b) => (Number(b.public_checks_pass) - Number(a.public_checks_pass)) || (a.flags - b.flags) || (a.words - b.words) || (a.i - b.i))
  J({ t: 'B', candidates: cands, selected: ok[0] ? ok[0].i : null })
  final = ok[0] ? { status: 'SELECTED', selected_dir: `${WS}/scratch/cand-${ok[0].i}/`, claims_done: ok[0].public_checks_pass && ok[0].flags === 0, output: `selected candidate ${ok[0].i}` } : { status: 'ERROR', claims_done: false, output: '' }
}
return { runId: A.runId, arm: A.arm, task: A.task, cap: CAP, calls, proxyCalls, final, journal }
