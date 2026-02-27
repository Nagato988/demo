#!/usr/bin/env python3
"""sop.py — Automates the Claude→Codex SOP loop.

Usage:
  ./sop.py "task description" [--validate "cmd"] [--file path] [--commit "msg"]
"""
import argparse
import datetime
import os
import re
import subprocess
import sys
import textwrap
import time

BRIDGE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bridge.sh")
MAX_RETRIES = 2

# ─── Section 1: CLI ──────────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(description="SOP v1 automation: route tasks to Codex or escalate to Claude.")
    p.add_argument("task", help="Task description")
    p.add_argument("--validate", metavar="CMD", help="Shell command that must exit 0 to accept Codex output")
    p.add_argument("--file", metavar="PATH", help="File path Codex must produce (Level 1 check)")
    p.add_argument("--commit", metavar="MSG", help="Git commit message on success (optional)")
    return p.parse_args()


def main():
    args = parse_args()
    task = args.task
    validate_cmd = args.validate
    file_path = args.file
    commit_msg = args.commit

    if not validate_cmd and not file_path:
        print("[sop] WARNING: No --validate or --file provided. Output will be accepted without verification.", file=sys.stderr)

    print(f"[sop] Task: {task}")
    route, reason = classify_task(task)
    print(f"[sop] Route: {route} ({reason})")

    if route == "CLAUDE":
        escalate(task=task, attempts=0, last_error="", reason=f"Classified as CLAUDE: {reason}")
        sys.exit(1)

    # CODEX path
    prompt = build_initial_prompt(task, validate_cmd, file_path)
    last_error = ""

    for attempt in range(1, MAX_RETRIES + 1):
        print(f"\n[sop] Attempt {attempt}/{MAX_RETRIES} → sending to Codex...")
        call_bridge(prompt)
        time.sleep(8)  # allow Codex to flush file writes before validation

        passed, last_error = run_validation(file_path, validate_cmd)

        if passed:
            print("[sop] Validation PASSED.")
            if commit_msg:
                git_commit(commit_msg, file_path)
            print("[sop] SUCCESS")
            sys.exit(0)

        print(f"[sop] Validation FAILED (attempt {attempt}):\n{last_error}")

        if attempt < MAX_RETRIES:
            print("[sop] Re-prompting Codex with fix template...")
            prompt = build_fix_prompt(task, last_error, validate_cmd, attempt)

    escalate(task=task, attempts=MAX_RETRIES, last_error=last_error)
    sys.exit(1)


# ─── Section 2: Classifier ───────────────────────────────────────────────────

CLAUDE_KEYWORDS = [
    "auth", "authentication", "authoriz", "permission",
    "secret", "password", "jwt", "oauth", "aes", "rsa", "hmac",
    "bcrypt", "scrypt", "argon", "ssl", "tls", "certificate",
    "architect", "design pattern", "data model", "api design",
    "trade-off", "tradeoff", "vulnerability", "injection",
    "review", "improve readability", "clean up",
]

VAGUE_PATTERNS = [
    "make it better", "follow our", "our style",
    "as needed", "where appropriate", "use your judgment",
]

CODEX_SIGNALS = [
    "create", "write", "implement", "add function", "add method",
    "rename", "move", "extract", "fix error", "fix bug",
    "fix failing", "run ", "execute", "grep", "find all",
    "docstring", "changelog", "readme", "test for",
    "regression test", "boilerplate", "refactor", "sort",
    "generate", "parse", "calculate", "convert",
]


def _word_match(keyword: str, text: str) -> bool:
    """Match keyword as whole word (or phrase) in text."""
    pattern = r'\b' + re.escape(keyword) + r'\b'
    return bool(re.search(pattern, text))


def classify_task(task: str) -> tuple[str, str]:
    t = task.lower()

    for kw in CLAUDE_KEYWORDS:
        if _word_match(kw, t):
            return "CLAUDE", f"security/architecture keyword: '{kw}'"

    for p in VAGUE_PATTERNS:
        if p in t:
            return "CLAUDE", f"vague intent pattern: '{p}'"

    for sig in CODEX_SIGNALS:
        if sig in t:
            return "CODEX", f"implementation signal: '{sig}'"

    return "CODEX", "default (no vague/security signals detected)"


# ─── Section 3: Prompt Builder ───────────────────────────────────────────────

def build_initial_prompt(task: str, validate_cmd: str | None, file_path: str | None) -> str:
    t = task.lower()

    if any(kw in t for kw in ["fix error", "fix bug", "fix failing", "stack trace"]):
        body = f"Fix error in the relevant file.\n{task}\nMinimal diff only."
    elif any(kw in t for kw in ["rename", "refactor"]):
        body = f"Apply this change:\n{task}\nNo behavior change. No other edits."
    elif any(kw in t for kw in ["regression test", "add test", "test for"]):
        body = f"Add regression test as specified:\n{task}\nDo not modify source files."
    elif any(kw in t for kw in ["run ", "execute", "grep", "find all"]):
        body = f"Run: {task}\nReport: stdout, exit code, and any errors.\nDo not modify files."
    else:
        file_line = f"at {file_path}" if file_path else "at the appropriate path"
        body = f"Create file {file_line}.\nRequirements:\n{task}"

    if validate_cmd:
        body += f"\nValidate: {validate_cmd}"

    return body


def build_fix_prompt(task: str, error_output: str, validate_cmd: str | None, attempt: int) -> str:
    MAX_ERROR_CHARS = 800
    truncated = error_output.strip()[:MAX_ERROR_CHARS]
    if len(error_output.strip()) > MAX_ERROR_CHARS:
        truncated += "\n... (truncated)"

    prompt = (
        f"Fix error. Attempt {attempt} of {MAX_RETRIES}.\n"
        f"Original task: {task}\n"
        f"Error:\n{truncated}\n"
        f"Minimal change only. Do not change other behavior."
    )
    if validate_cmd:
        prompt += f"\nValidate: {validate_cmd}"
    return prompt


# ─── Section 4: Bridge Caller ────────────────────────────────────────────────

def call_bridge(prompt: str) -> str:
    result = subprocess.run(
        [BRIDGE, prompt],
        capture_output=True,
        text=True,
    )
    output = result.stdout.strip()
    if output:
        print(f"[Codex] {output}")
    if result.returncode != 0:
        print(f"[sop] bridge.sh error: {result.stderr.strip()}", file=sys.stderr)
    return output


# ─── Section 5: Validator ────────────────────────────────────────────────────

def run_validation(file_path: str | None, validate_cmd: str | None) -> tuple[bool, str]:
    # Level 1 — file existence
    if file_path:
        if not os.path.exists(file_path):
            return False, f"Level 1 FAIL: File not found: {file_path}"
        if os.path.getsize(file_path) == 0:
            return False, f"Level 1 FAIL: File is empty: {file_path}"
        print(f"[sop] Level 1 PASS: {file_path} exists.")

    # Level 3 — validation command
    if validate_cmd:
        try:
            result = subprocess.run(
                validate_cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=120,
            )
        except subprocess.TimeoutExpired:
            return False, "Level 3 FAIL: Validation command timed out (120s)."

        if result.returncode != 0:
            combined = (result.stdout + "\n" + result.stderr).strip()
            return False, f"Level 3 FAIL (exit {result.returncode}):\n{combined}"

        print(f"[sop] Level 3 PASS: {validate_cmd}")

    return True, ""


# ─── Section 6: Escalation ───────────────────────────────────────────────────

def escalate(task: str, attempts: int, last_error: str, reason: str = "Codex failed after max retries") -> None:
    diff_output = _get_git_diff()
    report = textwrap.dedent(f"""
        ========== ESCALATION REPORT ==========
        Timestamp : {datetime.datetime.now().isoformat(timespec='seconds')}
        Reason    : {reason}
        Task      : {task}
        Attempts  : {attempts} / {MAX_RETRIES}
        Last error:
        {textwrap.indent(last_error.strip() or '(none)', '  ')}
        Git diff  :
        {textwrap.indent(diff_output or '(no changes)', '  ')}
        ========================================
        ACTION REQUIRED: Paste the above into Claude for diagnosis.
    """).strip()
    print(report, file=sys.stderr)


def _get_git_diff() -> str:
    try:
        result = subprocess.run(["git", "diff", "HEAD"], capture_output=True, text=True, timeout=10)
        return result.stdout.strip()
    except Exception:
        return "(git diff unavailable)"


# ─── Section 7: Git Helper ───────────────────────────────────────────────────

def git_commit(message: str, file_path: str | None) -> None:
    if file_path:
        subprocess.run(["git", "add", file_path], capture_output=True)
    result = subprocess.run(["git", "commit", "-am", message], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[sop] git commit failed: {result.stderr.strip()}", file=sys.stderr)
    else:
        print(f"[sop] Committed: {message}")


if __name__ == "__main__":
    main()
