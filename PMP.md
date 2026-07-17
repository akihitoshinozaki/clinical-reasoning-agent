# Clinical Reasoning Agent — Project Management Plan
 
*Re-baselined June 23, 2026. This is a working doc, not a deliverable. It lives in the repo.*
 
---
 
## 1. The goal, in one sentence
 
Build a working, honestly-evaluated **evidence-gated differential diagnosis system** that is credible enough to be the centerpiece of cold emails to healthcare-AI PIs — sent in time to land a **fall** lab position.
 
Everything below exists to serve that sentence. The system is the means; the lab position is the end.
 
---
 
## 2. Definition of done
 
The project is "done" when a PI skimming the repo for five minutes sees all five of these. Not before, and no extra credit for more.
 
1. **Correctly framed problem** — selective prediction / structural abstention under retrieval-grounded generation. (Not XAI, not accuracy improvement, not "make the LLM reason better.")
2. **A system that runs** — `/diagnose` works end-to-end with real retrieval and a real gate.
3. **An honest evaluation** — the ablation graph: gate-on vs gate-off, abstention rate vs accuracy.
4. **Clean, reproducible code** — public repo, working `requirements.txt`, README run instructions that actually work.
5. **An honestly-stated limitation** — the gate verifies evidence *exists*, not that it *applies to this patient*. Framed as the research frontier, not hidden as a bug.
 
If all five are true, the project is finished. Adding more is scope creep.
 
---
 
## 3. Scope
 
**In scope:** LLM Proposer → Retriever (PubMed) → deterministic Gate (`verify_spans` substring check) → abstain-or-emit. Evaluation on MTSamples notes. The ablation graph.
 
**Out of scope** (route to `v2_backlog.md`, do not build):
- UI / frontend of any kind
- Multiple LLM providers or model comparison
- Fine-tuning, RAG re-rankers, fancy retrieval
- Multi-turn dialogue, patient interaction
- Anything that verifies the evidence is *clinically correct for the patient* — that is the named limitation, not this project's job.
 
---
 
## 4. Schedule (re-baselined)
 
**Why re-baselined:** M1's original deadline (June 13) passed with `main.py` empty and `verify_spans()` unwritten. The slipped work is small — a stubbed `/diagnose` path plus a pure substring function — so the slip is deferral, not difficulty. The fix is to close M1 *this week* rather than shift the whole project 10 days.
 
| Milestone | Window | Done means |
|---|---|---|
| **M1 — skeleton** | by **Fri Jun 27** | stub retriever, `verify_spans()` written, `/diagnose` passes end-to-end, `requirements.txt` fixed |
| **M2 — real pipeline** | **Jun 28 – Jul 11** | real PubMed retrieval + real gate working on actual notes |
| **M3 — ship** | **Jul 12 – Jul 31** | ablation eval run, graph produced, repo public and reproducible |
| **Outreach prep** | **Aug 1 – Aug 10** | PI paper deep-reading + cold email drafts |
| **Send** | **mid–late Aug** | emails out while fall positions are still being decided |
 
**The keystone:** this schedule keeps the fall goal alive *only if M1 closes by Friday.* If M1 slips again, the fall timeline is what breaks — not M2 or M3. That is the single load-bearing assumption in this whole plan.
 
---
 
## 5. Critical path
 
The thesis is the ablation graph. Trace what it depends on, backward:
 
```
ablation graph
  ← eval harness (accuracy + abstention metrics on a labeled set)
  ← working gate (so it can be toggled on/off)
      ← real retriever (real evidence to check against)
      ← verify_spans()   ← depends on NOTHING. pure function. currently unwritten.
```
 
`verify_spans()` sits at the bottom of the chain, blocks everything above it, and is the cheapest thing to write. **It is the literal next action.**
 
---
 
## 6. Work breakdown — next concrete tasks (small, in order)
 
1. Write `verify_spans(spans, note)` → deterministic `norm(e) in note` substring check. ~20 lines.
2. Fill `requirements.txt` so the README's run instructions work.
3. Wire `main.py`: stub retriever → proposer → `verify_spans` gate → `/diagnose` returns or abstains.
4. Run `/diagnose` once end-to-end on one MTSamples note. **M1 closed.**
5. (M2) Replace stub with real PubMed retrieval.
 
Do #1 before reading any further. The plan is worth nothing until it exists.
 
---
 
## 7. Risks & mitigations
 
| Risk | Why it's real | Mitigation |
|---|---|---|
| **Schedule slip from deferring small tasks** | M1 already slipped this way | Sunday checklist; two consecutive failing weeks → cut scope, not extend deadline |
| **Scope creep** | killed prior projects (DTI) | hard out-of-scope list (§3); every new idea → `v2_backlog.md`, never the codebase |
| **Null ablation result** — gate doesn't improve the tradeoff | a PI *will* ask this | a negative result is still a finding; the contribution is "structural abstention is achievable," not "gate raises accuracy." Report it honestly either way. |
| **No clean labels in MTSamples** | you can't measure "accuracy" without ground-truth diagnoses | confirm label availability *during M2*, not M3. If absent, define the accuracy metric early (e.g. hand-label a small held-out set) or narrow the claim to abstention behavior. |
 
---
 
## 8. Cadence & control
 
- **Every Sunday:** check the week's task against this plan. Done / not done. No narrative.
- **Two consecutive failing weeks:** scope gets cut (drop something from §3-in to §3-out). The deadline does not move — the fall position is a fixed external date.
- **Definition of "shipping" beats definition of "impressive."** Complexity is not a metric here. A finished simple thing emails well; an unfinished sophisticated thing does not exist.
