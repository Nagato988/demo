# Claude + Codex Delegation Strategy

## Overview

This project uses a two-agent setup: Claude Sonnet 4.6 (orchestrator) and GPT-5.3-Codex (executor),
communicating via `bridge.sh` over tmux.

## What to Delegate to Codex (GPT-5.3-Codex)

- **Pure implementation** — writing boilerplate, generating functions from clear specs, creating files
- **Running commands & verifying output** — Codex autonomously executes and sanity-checks its own work
- **Documentation & boilerplate** — GPT-5 leads Claude in documentation and boilerplate-heavy generation
- **Repetitive refactors** — mechanical transformations (renaming, reformatting, restructuring)

## What Claude Handles

- **Architecture & design decisions** — reasoning about tradeoffs and nuanced requirements
- **Debugging complex logic** — Claude Sonnet 4.6 edges ahead in refactoring and debugging
- **Understanding user intent** — interpreting ambiguous instructions before delegating a precise spec
- **Code review** — reviewing Codex's output for correctness, security, and style

## Optimal Workflow

```
User → Claude (understand intent, design, review)
              ↓ precise spec
           Codex (implement, run, verify)
              ↓ result
           Claude (review & approve)
              ↓
            User
```

## Benchmark Justification

- On SWE-bench Verified, Claude Sonnet 4.6 scores 77.2% vs Codex at 74.5% — Claude is stronger at complex reasoning
- In a 15-task developer benchmark, GPT-5 led in documentation/boilerplate; Claude led in debugging/refactoring
- GPT-5.3-Codex achieves top scores on Terminal-Bench — confirming its strength as a CLI executor

## Sources

- [Introducing GPT-5.3-Codex | OpenAI](https://openai.com/index/introducing-gpt-5-3-codex/)
- [Claude Sonnet 4.6 vs. GPT-5: The 2026 Developer Benchmark | SitePoint](https://www.sitepoint.com/claude-sonnet-4-6-vs-gpt-5-the-2026-developer-benchmark/)
- [LiveCodeBench Leaderboard](https://livecodebench.github.io/leaderboard.html)
- [SWE-bench Results Viewer](https://www.swebench.com/viewer.html)
- [GPT-5.3-Codex System Card | OpenAI](https://openai.com/index/gpt-5-3-codex-system-card/)
