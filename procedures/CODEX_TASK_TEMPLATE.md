# CODEX_TASK_TEMPLATE.md — Minimal Prompt Templates

## Rules for Prompting Codex

- Be unambiguous. No open-ended instructions.
- Always specify: what, where, and how to validate.
- No context padding. No explanation of why.
- One task per prompt.

---

## Templates

### 1. Create a file

```
Create [filename] at [path].
Requirements:
- [bullet spec]
- [bullet spec]
Validate: [command that must exit 0]
```

**Example:**
```
Create utils/slugify.py at /home/nagato98/projects/demo/utils/slugify.py.
Requirements:
- Function slugify(text: str) -> str
- Lowercase, replace spaces with hyphens, strip non-alphanumeric
Validate: python3 -c "from utils.slugify import slugify; assert slugify('Hello World') == 'hello-world'"
```

---

### 2. Fix an error

```
Fix error in [file]:[line].
Error: [exact error message]
Do not change other behavior. Minimal diff only.
Validate: [command]
```

---

### 3. Add a regression test

```
Add regression test in [test_file] for [function/case].
Test must fail before fix, pass after.
Do not modify source files.
Validate: [test command]
```

---

### 4. Refactor / rename

```
In [file], rename [old] to [new] everywhere.
No behavior change. No other edits.
Validate: [lint or test command]
```

---

### 5. Patch only (minimal diff)

```
Minimal patch for: [issue description]
File: [path]
Constraint: change as few lines as possible.
Validate: [command]
```

---

### 6. Run and report

```
Run: [command]
Report: stdout, exit code, and any errors.
Do not modify files.
```

---

### 7. Search / grep

```
Find all occurrences of [pattern] in [directory].
Report: file path, line number, line content.
Do not modify files.
```

---

## Anti-patterns (never send these to Codex)

- "Improve the code" — too vague
- "Refactor for readability" — no measurable criterion
- "Fix the bug" — no error message provided
- Multi-task prompts — split into separate calls
