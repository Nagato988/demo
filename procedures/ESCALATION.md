# ESCALATION.md — When and How to Escalate to Claude

## Escalation Triggers

| Trigger | Threshold | Action |
|---------|-----------|--------|
| Codex failed same task | ≥ 2 attempts | Escalate immediately |
| Ambiguous requirement detected | Any | Claude clarifies, re-routes |
| Security-sensitive pattern found | Any | Claude reviews before merge |
| Architecture impact detected | Any | Claude decides approach first |
| Test suite regression (new failures) | Any | Claude diagnoses root cause |
| Codex output contradicts the spec | Any | Claude arbitrates |
| Task scope expanded mid-execution | Any | Claude re-classifies |

---

## Escalation Protocol

### Step 1 — Collect context (cheap)

Before handing off to Claude, gather:

```bash
# What Codex produced
git diff HEAD

# What failed
[last error message / test output]

# How many attempts were made
[count]
```

### Step 2 — Escalation prompt to Claude (minimal)

```
ESCALATION
Task: [one-line description]
Attempts: [N]
Last error: [exact error or symptom]
Diff so far: [git diff or "none"]
Question: [specific thing Claude must decide or fix]
```

Keep it under 10 lines. No padding.

### Step 3 — Claude responds with one of:

- **FIX**: Claude provides the fix directly
- **RE-ROUTE**: Claude rewrites the Codex prompt and re-delegates
- **ABORT**: Task is out of scope or requires user input

---

## Escalation Decision Tree

```
Codex output received
       │
       ▼
Validation passed? ──YES──► Commit
       │
       NO
       ▼
Attempt < 2? ──YES──► Re-prompt Codex (fix template)
       │
       NO
       ▼
Is it a security/arch issue? ──YES──► Claude reviews immediately
       │
       NO
       ▼
Claude diagnoses with diff only ──► Fix or Abort
```

---

## What Claude Does NOT Do During Escalation

- Does not re-read entire codebase (use diff only)
- Does not rewrite working code
- Does not second-guess Codex on mechanical tasks it passed
- Does not explain reasoning to Codex (Codex gets a corrected prompt only)

---

## Escalation Outcomes

| Outcome | Next action |
|---------|-------------|
| Claude fixes directly | Commit, close loop |
| Claude re-prompts Codex | Restart validation from Level 1 |
| Requires user input | Surface question to user (max 1 question) |
| Out of scope | Abort, document why, notify user |
