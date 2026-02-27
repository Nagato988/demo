# ROUTING.md — When to Use Codex vs Claude

## Benchmark Basis

| Metric              | Claude Sonnet 4.6 | GPT-5.3-Codex |
|---------------------|-------------------|---------------|
| SWE-bench Verified  | 77.2%             | 74.5%         |
| Terminal-Bench      | lower             | best-in-class |
| Debugging/Refactor  | stronger          | weaker        |
| Boilerplate/Docs    | weaker            | stronger      |
| Math reasoning      | strong            | 100% AIME     |

Sources: [LiveBench](https://livebench.ai) · [LM Council](https://lmcouncil.ai/benchmarks) · [SWE-bench](https://www.swebench.com/viewer.html)

---

## Decision Table

### ROUTE TO CODEX (delegate, low cost)

| Signal | Examples |
|--------|----------|
| Clear spec, single file | "Create X that does Y, validate with Z" |
| Mechanical transformation | rename, reformat, sort, extract constant |
| Boilerplate generation | CRUD, tests for known functions, configs |
| Run & verify | execute script, run linter, run tests |
| Documentation | docstrings, README sections, changelogs |
| Simple bug with error message | stack trace + file path provided |
| grep / search task | find usages, list TODOs, count lines |

### ROUTE TO CLAUDE (keep, higher cost justified)

| Signal | Examples |
|--------|----------|
| Ambiguous user intent | vague requirement, no clear spec |
| Architectural decision | choosing patterns, data models, APIs |
| Security-sensitive code | auth, crypto, input validation |
| Complex multi-file refactor | behavior must be preserved across N files |
| Reviewing Codex output | correctness, security, edge cases |
| Repeated Codex failures (≥2) | same task failed twice → escalate |
| Cross-cutting concerns | performance, observability, error strategy |

### REQUIRES VALIDATION (borderline)

| Signal | Action |
|--------|--------|
| Multi-file with side effects | Codex executes, Claude reviews diff |
| New external API integration | Codex drafts, Claude checks contract |
| Optimization task | Codex implements, validate with benchmark |
| Unfamiliar codebase area | run fast checks before accepting |

---

## Router Decision Loop

```
User task
   │
   ▼
[1] Claude classifies task (1–3 sentences max)
   │
   ├─ CODEX → build minimal prompt → bridge.sh → validate
   │              │
   │              ├─ PASS → commit
   │              └─ FAIL → low-cost debug → re-prompt (max 2x) → escalate if still failing
   │
   ├─ CLAUDE → Claude executes directly
   │
   └─ VALIDATE → Codex executes → Claude reviews diff only
```

---

## Classification Heuristics (fast, token-cheap)

Ask these in order, stop at first YES:

1. Is the spec fully unambiguous and self-contained? → **Codex**
2. Does it touch security, auth, or architecture? → **Claude**
3. Does it require running/verifying something? → **Codex**
4. Did Codex already fail this task once? → **Claude**
5. Is it a review of existing output? → **Claude**
6. Otherwise → **Codex** with validation step
