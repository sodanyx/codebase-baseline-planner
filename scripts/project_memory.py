#!/usr/bin/env python3
"""Initialize and inspect persistent AI project-context documents.

This utility never overwrites existing Markdown documents unless --force is used.
It records repository revision metadata in JSON so later agents can decide whether
full, incremental, or no rescanning is required.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ENTRYPOINT = "AI_PROJECT_CONTEXT.md"
MEMORY_DIR = Path("docs") / "ai-project"
STATE_FILE = MEMORY_DIR / "state.json"
REQUIRED_DOCS = {
    "baseline": MEMORY_DIR / "BASELINE.md",
    "decisions": MEMORY_DIR / "DECISIONS.md",
    "fusion_plan": MEMORY_DIR / "FUSION_PLAN.md",
    "implementation_status": MEMORY_DIR / "IMPLEMENTATION_STATUS.md",
    "changelog": MEMORY_DIR / "CHANGELOG.md",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def run_git(root: Path, *args: str) -> tuple[int, str]:
    try:
        proc = subprocess.run(
            ["git", "-C", str(root), *args],
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return 127, ""
    return proc.returncode, proc.stdout.rstrip("\n")


def resolve_root(value: str | None) -> Path:
    candidate = Path(value or ".").expanduser().resolve()
    code, output = run_git(candidate, "rev-parse", "--show-toplevel")
    if code == 0 and output:
        return Path(output).resolve()
    return candidate


def is_context_path(value: str) -> bool:
    normalized = value.replace("\\", "/").lstrip("./")
    return normalized == ENTRYPOINT or normalized.startswith(str(MEMORY_DIR).replace("\\", "/") + "/")


def parse_status_paths(status: str) -> tuple[list[str], list[str]]:
    source_paths: list[str] = []
    context_paths: list[str] = []
    for line in status.splitlines():
        if not line:
            continue
        value = line[3:] if len(line) >= 4 else line
        if " -> " in value:
            value = value.split(" -> ", 1)[1]
        target = context_paths if is_context_path(value) else source_paths
        target.append(value)
    return sorted(set(source_paths)), sorted(set(context_paths))


def git_snapshot(root: Path) -> dict[str, Any]:
    head_code, head = run_git(root, "rev-parse", "HEAD")
    branch_code, branch = run_git(root, "branch", "--show-current")
    status_code, status = run_git(root, "status", "--porcelain", "--untracked-files=all")
    source_paths, context_paths = parse_status_paths(status) if status_code == 0 else ([], [])
    return {
        "is_git_repository": head_code == 0,
        "head": head if head_code == 0 else None,
        "branch": branch if branch_code == 0 and branch else None,
        "worktree_dirty": bool(status) if status_code == 0 else None,
        "source_worktree_dirty": bool(source_paths) if status_code == 0 else None,
        "context_worktree_dirty": bool(context_paths) if status_code == 0 else None,
        "source_worktree_paths": source_paths,
        "context_worktree_paths": context_paths,
    }


def default_state(root: Path) -> dict[str, Any]:
    snapshot = git_snapshot(root)
    return {
        "schema_version": 1,
        "project_root": str(root),
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "current_phase": "baseline-not-started",
        "baseline_revision": None,
        "last_reviewed_revision": None,
        "fusion_plan_revision": None,
        "implementation_revision": None,
        "source_branch": snapshot["branch"],
        "notes": "Revision fields are updated only after the corresponding document has been reviewed.",
    }


def templates(project_name: str) -> dict[Path, str]:
    return {
        Path(ENTRYPOINT): f"""# {project_name} AI Project Context\n\n> This is the stable entrypoint for agents resuming work on this repository.\n\n## Read first\n\n1. `docs/ai-project/state.json` — revision and freshness metadata\n2. `docs/ai-project/BASELINE.md` — original-project architecture and evidence baseline\n3. `docs/ai-project/DECISIONS.md` — confirmed, rejected, deferred, and pending decisions\n4. `docs/ai-project/FUSION_PLAN.md` — confirmed integrated architecture and implementation plan\n5. `docs/ai-project/IMPLEMENTATION_STATUS.md` — completed, in-progress, blocked, and remaining work\n6. `docs/ai-project/CHANGELOG.md` — history of context-document updates\n\n## Current handoff\n\n- Current phase: baseline not started\n- Last reviewed source revision: not recorded\n- Immediate next action: establish the original-project baseline\n- Blocking issues: none recorded\n\nDo not trust this summary alone. Compare the repository state with `state.json`, then reuse or incrementally refresh the detailed documents.\n""",
        REQUIRED_DOCS["baseline"]: f"""# {project_name} Original-Project Baseline\n\n## Document status\n\n- Source branch: not recorded\n- Source revision: not recorded\n- Last reviewed: not recorded\n- Coverage boundary: not recorded\n\n## Executive summary\n\nNot analyzed yet.\n\n## Project purpose and boundaries\n\nNot analyzed yet.\n\n## Architecture and complete runtime flow\n\nNot analyzed yet.\n\n## Code map and key conventions\n\nNot analyzed yet.\n\n## Environment, dependencies, build, and deployment\n\nNot analyzed yet.\n\n## Tests, diagnostics, and quality controls\n\nNot analyzed yet.\n\n## Repository history and reusable lessons\n\nNot analyzed yet.\n\n## High-impact constraints and unsafe modification areas\n\nNot analyzed yet.\n\n## Evidence status and unresolved unknowns\n\nNot analyzed yet.\n""",
        REQUIRED_DOCS["decisions"]: f"""# {project_name} Decision Log\n\nUse stable IDs such as `DEC-001`. Never delete rejected or superseded decisions; append a status change and reason.\n\n| ID | Date | Topic | Status | Decision | Evidence / rationale | Revisit condition |\n|---|---|---|---|---|---|---|\n| DEC-001 | not recorded | Initial scope | pending | Awaiting discussion | — | User confirmation |\n""",
        REQUIRED_DOCS["fusion_plan"]: f"""# {project_name} Confirmed Fusion Plan\n\n## Document status\n\n- Confirmation state: not confirmed\n- Source baseline revision: not recorded\n- Last updated: not recorded\n\nDo not treat candidate ideas as confirmed architecture. Populate this file only after explicit user confirmation.\n""",
        REQUIRED_DOCS["implementation_status"]: f"""# {project_name} Implementation Status\n\n## Current summary\n\n- Current phase: not started\n- Last implementation revision: not recorded\n- Next action: wait for a confirmed fusion plan\n- Blockers: none recorded\n\n## Work items\n\nUse stable IDs such as `IMP-001`. Mark an item completed only when code and verification evidence are recorded.\n\n| ID | Related decision | Work item | Status | Files / commits | Verification | Remaining work / next action |\n|---|---|---|---|---|---|---|\n| IMP-001 | — | Establish implementation plan | not-started | — | — | Confirm fusion plan |\n\n## Known defects and regressions\n\nNone recorded.\n\n## Handoff notes\n\nNo implementation handoff recorded.\n""",
        REQUIRED_DOCS["changelog"]: f"""# {project_name} Context Documentation Changelog\n\nRecord meaningful changes to the baseline, decisions, plan, or implementation state.\n\n| Date | Source revision | Documents changed | Reason | Agent / author |\n|---|---|---|---|---|\n| {now_iso()} | not recorded | Initial scaffold | Created persistent project-context structure | automated scaffold |\n""",
    }


def write_text(path: Path, content: str, force: bool) -> str:
    if path.exists() and not force:
        return "kept"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return "written"


def load_state(root: Path) -> dict[str, Any] | None:
    path = root / STATE_FILE
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def save_state(root: Path, state: dict[str, Any]) -> None:
    path = root / STATE_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def command_init(args: argparse.Namespace) -> int:
    root = resolve_root(args.project_root)
    root.mkdir(parents=True, exist_ok=True)
    project_name = args.project_name or root.name
    results: dict[str, str] = {}
    for relative, content in templates(project_name).items():
        results[str(relative)] = write_text(root / relative, content, args.force)

    state = load_state(root)
    if state is None or args.force:
        state = default_state(root)
        save_state(root, state)
        results[str(STATE_FILE)] = "written"
    else:
        results[str(STATE_FILE)] = "kept"

    print(json.dumps({"project_root": str(root), "files": results}, ensure_ascii=False, indent=2))
    return 0


def changed_files(
    root: Path,
    revision: str | None,
    worktree_source_paths: list[str] | None = None,
) -> tuple[str, list[str]]:
    if not revision:
        return "unknown", sorted(set(worktree_source_paths or []))
    code, _ = run_git(root, "cat-file", "-e", f"{revision}^{{commit}}")
    if code != 0:
        return "invalid-recorded-revision", sorted(set(worktree_source_paths or []))
    code, output = run_git(root, "diff", "--name-only", revision, "--")
    if code != 0:
        return "git-diff-failed", sorted(set(worktree_source_paths or []))
    files = [line for line in output.splitlines() if line and not is_context_path(line)]
    files.extend(worktree_source_paths or [])
    unique = sorted(set(files))
    return ("changed" if unique else "same"), unique


def command_status(args: argparse.Namespace) -> int:
    root = resolve_root(args.project_root)
    state = load_state(root)
    snapshot = git_snapshot(root)
    recorded = None if state is None else state.get("last_reviewed_revision") or state.get("baseline_revision")
    freshness, files = changed_files(root, recorded, snapshot.get("source_worktree_paths") or [])
    required = [Path(ENTRYPOINT), STATE_FILE, *REQUIRED_DOCS.values()]
    missing = [str(path) for path in required if not (root / path).exists()]
    result = {
        "project_root": str(root),
        "state_found": state is not None,
        "recorded_revision": recorded,
        "current_repository": snapshot,
        "freshness": freshness,
        "changed_files_since_review": files,
        "missing_required_files": missing,
        "recommended_action": recommend_action(state, snapshot, freshness, files, missing),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def recommend_action(
    state: dict[str, Any] | None,
    snapshot: dict[str, Any],
    freshness: str,
    files: list[str],
    missing: list[str],
) -> str:
    if state is None or missing:
        return "initialize-or-repair-project-memory-and-establish-baseline"
    if not snapshot["is_git_repository"]:
        return "reuse-documents-but-manually-verify-source-freshness"
    if freshness == "same" and not snapshot["source_worktree_dirty"]:
        return "reuse-existing-context-without-full-rescan"
    if freshness == "changed" or snapshot["source_worktree_dirty"]:
        if len(files) <= 50:
            return "perform-targeted-incremental-review"
        return "perform-broader-review-because-change-set-is-large"
    return "verify-recorded-revision-and-consider-full-baseline-review"


def command_stamp(args: argparse.Namespace) -> int:
    root = resolve_root(args.project_root)
    state = load_state(root) or default_state(root)
    snapshot = git_snapshot(root)
    revision = args.revision or snapshot.get("head")
    if not revision and not args.allow_no_revision:
        print("Cannot stamp without a Git revision; pass --allow-no-revision for non-Git projects.", file=sys.stderr)
        return 2

    state["updated_at"] = now_iso()
    state["source_branch"] = snapshot.get("branch")
    state["current_phase"] = args.phase
    state["last_reviewed_revision"] = revision
    if args.phase == "baseline-complete":
        state["baseline_revision"] = revision
    elif args.phase == "fusion-plan-confirmed":
        state["fusion_plan_revision"] = revision
    elif args.phase in {"implementation-in-progress", "implementation-complete"}:
        state["implementation_revision"] = revision
    save_state(root, state)
    print(json.dumps(state, ensure_ascii=False, indent=2))
    return 0


def command_validate(args: argparse.Namespace) -> int:
    root = resolve_root(args.project_root)
    state = load_state(root)
    required = [Path(ENTRYPOINT), STATE_FILE, *REQUIRED_DOCS.values()]
    missing = [str(path) for path in required if not (root / path).exists()]
    errors: list[str] = []
    if state is None:
        errors.append("state.json is missing or invalid JSON")
    elif state.get("schema_version") != 1:
        errors.append("unsupported or missing schema_version")
    if missing:
        errors.append("missing files: " + ", ".join(missing))
    result = {"valid": not errors, "errors": errors, "project_root": str(root)}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create the persistent project-context scaffold")
    init_parser.add_argument("--project-root")
    init_parser.add_argument("--project-name")
    init_parser.add_argument("--force", action="store_true")
    init_parser.set_defaults(func=command_init)

    status_parser = subparsers.add_parser("status", help="Compare saved context metadata with the current repository")
    status_parser.add_argument("--project-root")
    status_parser.set_defaults(func=command_status)

    stamp_parser = subparsers.add_parser("stamp", help="Record a reviewed project phase and source revision")
    stamp_parser.add_argument("--project-root")
    stamp_parser.add_argument(
        "--phase",
        required=True,
        choices=[
            "baseline-not-started",
            "baseline-in-progress",
            "baseline-complete",
            "ideas-under-review",
            "fusion-plan-confirmed",
            "implementation-in-progress",
            "implementation-complete",
            "maintenance",
        ],
    )
    stamp_parser.add_argument("--revision")
    stamp_parser.add_argument("--allow-no-revision", action="store_true")
    stamp_parser.set_defaults(func=command_stamp)

    validate_parser = subparsers.add_parser("validate", help="Validate the project-context scaffold")
    validate_parser.add_argument("--project-root")
    validate_parser.set_defaults(func=command_validate)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
