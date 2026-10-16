#!/usr/bin/env python3
"""Clone all member repositories of this multi-repo workspace.

This root repo ("delivery-workspace") only tracks docs/ and this script;
each of the folders below is an independent git repository. Run this
script after cloning the workspace to fetch all of them.

Usage:
    python workspace.py                # clone missing repos
    python workspace.py --update       # also `git pull` repos that already exist
    python workspace.py --only demo-front,demo-back-api
    python workspace.py --list         # print the manifest and exit
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPOS: dict[str, str] = {
    "delivery-cli": "https://github.com/jhidalgo3/delivery-cli.git",
    "delivery-github-workflow": "https://github.com/jhidalgo3/delivery-github-workflow.git",
    "demo-back-api": "https://github.com/jhidalgo3/demo-back-api.git",
    "demo-e2e": "https://github.com/jhidalgo3/demo-e2e.git",
    "demo-front": "https://github.com/jhidalgo3/demo-front.git",
    "demo-specs": "https://github.com/jhidalgo3/demo-specs.git",
}

WORKSPACE_ROOT = Path(__file__).resolve().parent


def clone(name: str, url: str) -> None:
    target = WORKSPACE_ROOT / name
    if (target / ".git").is_dir():
        print(f"[skip]  {name} already cloned")
        return
    print(f"[clone] {name} <- {url}")
    subprocess.run(["git", "clone", url, str(target)], check=True)


def update(name: str) -> None:
    target = WORKSPACE_ROOT / name
    if not (target / ".git").is_dir():
        print(f"[warn]  {name} not cloned yet, skipping update")
        return
    print(f"[pull]  {name}")
    subprocess.run(["git", "-C", str(target), "pull", "--ff-only"], check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--update", action="store_true", help="git pull repos that are already cloned")
    parser.add_argument("--only", help="comma-separated subset of repo names to process")
    parser.add_argument("--list", action="store_true", help="print the manifest and exit")
    args = parser.parse_args()

    if args.list:
        for name, url in REPOS.items():
            print(f"{name}\t{url}")
        return 0

    names = args.only.split(",") if args.only else list(REPOS)
    unknown = [n for n in names if n not in REPOS]
    if unknown:
        print(f"error: unknown repo(s): {', '.join(unknown)}", file=sys.stderr)
        return 1

    for name in names:
        clone(name, REPOS[name])
        if args.update:
            update(name)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
