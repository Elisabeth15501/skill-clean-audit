#!/usr/bin/env python3
"""
clean_code_clawhub_export.py
Build a ClawHub-compliant publish copy of skill-clean-audit from the dev source.

What it does (per clean_code_clawhub_publish_plan.md, sources S1-S5):
  1. Copy every file except .git
  2. Apply .clawhubignore (LICENSE, *.skill, __pycache__/ ...)
  3. Drop README.md (S2: no README inside the skill folder)
  4. Strip frontmatter fields license:/slug:/displayName: (S1/S5)
  5. Sanitize any C:\\Users\\elisa absolute path -> ~/  (privacy)
  6. Print an audit trail of every transformation

The SOURCE repo is never modified. Only the --out directory is written.

Usage:
  python clean_code_clawhub_export.py --src <dev skill dir> --out <temp dir>
"""
import argparse
import fnmatch
import os
import re
import shutil

STRIP_FRONTMATTER_FIELDS = ("license:", "slug:", "displayName:")
USERNAME_PATH_RE = re.compile(r"C:[\\/]Users[\\/]elisa(?=[\\/]|$)")
README_NAME = "README.md"


def parse_clawhubignore(src: str) -> list[str]:
    """Return a list of ignore patterns from .clawhubignore (comments/blank skipped)."""
    p = os.path.join(src, ".clawhubignore")
    if not os.path.isfile(p):
        return []
    pats = []
    with open(p, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            pats.append(line)
    return pats


def is_ignored(rel: str, is_dir: bool, patterns: list[str]) -> bool:
    """Minimal gitignore matcher: exact name, trailing-slash dir, or glob on basename."""
    base = os.path.basename(rel.rstrip("/\\"))
    for pat in patterns:
        # directory pattern like "__pycache__/"
        if pat.endswith("/"):
            dirname = pat.rstrip("/\\")
            if is_dir and (base == dirname or rel.rstrip("/\\").endswith(dirname)):
                return True
            continue
        # glob on basename
        if ("*" in pat or "?" in pat) and fnmatch.fnmatch(base, pat):
            return True
        # exact basename
        if base == pat or rel == pat:
            return True
    return False


def strip_frontmatter_fields(text: str) -> str:
    """Remove specific top-level frontmatter lines (license:/slug:/displayName:)."""
    if not text.startswith("---"):
        return text
    end = text.find("\n---", 3)
    if end == -1:
        return text
    head = text[: end + 4]
    body = text[end + 4 :]
    kept = []
    for line in head.splitlines(keepends=True):
        stripped = line.lstrip()
        if any(stripped.startswith(f) for f in STRIP_FRONTMATTER_FIELDS):
            continue
        kept.append(line)
    return "".join(kept) + body


def sanitize_username(text: str) -> str:
    return USERNAME_PATH_RE.sub("~", text)


def main() -> None:
    ap = argparse.ArgumentParser(description="Build a ClawHub-compliant export of skill-clean-audit")
    ap.add_argument("--src", required=True, help="dev source skill directory")
    ap.add_argument("--out", required=True, help="output (clean) directory to write")
    args = ap.parse_args()

    src = os.path.abspath(args.src)
    out = os.path.abspath(args.out)
    if not os.path.isdir(src):
        raise SystemExit(f"source not found: {src}")
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out, exist_ok=True)

    patterns = parse_clawhubignore(src)
    log = []

    for root, dirs, files in os.walk(src):
        rel_root = os.path.relpath(root, src)
        # skip .git entirely
        if ".git" in dirs:
            dirs.remove(".git")
        # filter ignored dirs
        kept_dirs = []
        for d in dirs:
            rel = os.path.normpath(os.path.join(rel_root, d)).replace(os.sep, "/")
            if is_ignored(rel, True, patterns):
                log.append(f"IGNORE dir : {rel}/")
                continue
            kept_dirs.append(d)
        dirs[:] = kept_dirs

        for fn in files:
            rel = os.path.normpath(os.path.join(rel_root, fn)).replace(os.sep, "/")
            if rel == ".gitignore" or rel.startswith(".git/"):
                continue  # never copy git internals
            if is_ignored(rel, False, patterns):
                log.append(f"IGNORE file: {rel}")
                continue
            if fn == README_NAME:
                log.append(f"DROP README: {rel}  (S2: no README inside skill folder)")
                continue
            src_file = os.path.join(root, fn)
            dst_file = os.path.join(out, rel)
            os.makedirs(os.path.dirname(dst_file), exist_ok=True)
            if fn.lower().endswith((".md", ".html", ".txt", ".json", ".yaml", ".yml")):
                with open(src_file, encoding="utf-8") as f:
                    txt = f.read()
                if fn == "SKILL.md":
                    txt = strip_frontmatter_fields(txt)
                    log.append("STRIP frontmatter: license:/slug:/displayName:  (S1/S5)")
                if USERNAME_PATH_RE.search(txt):
                    txt = sanitize_username(txt)
                    log.append(f"SANITIZE path: C:\\Users\\elisa -> ~/  in {rel}")
                with open(dst_file, "w", encoding="utf-8", newline="") as f:
                    f.write(txt)
            else:
                shutil.copy2(src_file, dst_file)

    print("=== ClawHub export built ===")
    print(f"source : {src}")
    print(f"output : {out}")
    print("--- transformations ---")
    print("\n".join(log) if log else "(none)")
    print("--- resulting tree ---")
    for r, _, fs in os.walk(out):
        for f in sorted(fs):
            print("  " + os.path.relpath(os.path.join(r, f), out).replace(os.sep, "/"))
    print("\nNext: review the tree, then `clawhub publish <out> --slug skill-clean-audit "
          "--name \"First-Principles Clean Code Audit\" --version <ver>`")


if __name__ == "__main__":
    main()
