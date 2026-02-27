# VALIDATION.md — Cheap Debugging and Output Checks

## Principle

Run cheapest checks first. Escalate to semantic reasoning only if they pass
but output is still suspected wrong.

---

## Validation Ladder (cheapest → most expensive)

### Level 1 — Structure (free, instant)

- File exists at expected path
- File is non-empty
- Expected symbols present: `grep -n "def " file.py`
- No syntax errors: `python3 -m py_compile file.py` / `node --check file.js`

**If Level 1 fails:** re-prompt Codex with exact error. Do not escalate yet.

---

### Level 2 — Lint + Format (cheap)

```bash
# Python
ruff check file.py
black --check file.py

# JavaScript
eslint file.js

# Shell
shellcheck script.sh
```

**If Level 2 fails:** send Codex the lint output using the "fix error" template.

---

### Level 3 — Tests (medium cost, high signal)

```bash
# Run existing tests
python3 -m pytest tests/ -x -q

# Run only affected test
python3 -m pytest tests/test_target.py -x -q

# Check exit code
echo "Exit: $?"
```

**If Level 3 fails:** check if test failure is in new code or pre-existing.
- Pre-existing → ignore, note it, continue
- New code → re-prompt Codex with: `Fix failing test: [test name]. Error: [output]`

---

### Level 4 — Behavioral spot-check (medium cost)

Run a minimal smoke test manually:

```bash
python3 -c "[import and call the new function with known input]"
```

Compare output to expectation. If wrong → re-prompt Codex.

---

### Level 5 — Semantic review (expensive, Claude only)

Only reach here if Levels 1–4 pass but output is still suspect (e.g. logic
seems off, security concern flagged by grep).

Claude reads the diff and reasons about correctness. This is the escalation
point.

---

## Quick Grep Checks (use before Level 5)

```bash
# Detect hardcoded secrets
grep -rn "password\|secret\|token\|api_key" --include="*.py" .

# Detect TODO/FIXME left in new code
git diff HEAD | grep -i "todo\|fixme\|hack\|xxx"

# Check for obvious bad patterns
grep -n "eval(\|exec(\|os.system(" file.py
```

---

## Re-prompt Strategy

| Failure | Re-prompt template |
|---------|-------------------|
| Syntax error | `Fix syntax error in [file]:[line]. Error: [msg]. Minimal change only.` |
| Lint error | `Fix lint: [rule] in [file]:[line]. Do not change other code.` |
| Test failure | `Fix failing test [name]. Error: [output]. Do not change other tests.` |
| Wrong output | `Output was [actual], expected [expected]. Fix [function] in [file].` |

**Max re-prompts: 2.** If still failing after 2 attempts → escalate to Claude.

---

## Acceptance Criteria (task is done when)

- [ ] File exists and is non-empty
- [ ] No syntax errors
- [ ] Lint passes (or pre-existing failures only)
- [ ] Relevant tests pass
- [ ] Smoke test produces expected output
- [ ] No new secrets/dangerous patterns introduced
