#!/usr/bin/env python3
"""
Scan GitHub repos for Claude Code skills, CLAUDE.md, and AGENTS.md files.
Outputs a master inventory of all AI-native artifacts across repos.

Usage:
    python scan-skills.py                    # Scan PacerAI org + personal repos
    python scan-skills.py --org PacerAI      # Scan only PacerAI org
    python scan-skills.py --user wsullivan-dev  # Scan only personal repos
    python scan-skills.py --local            # Scan local ~/Documents/GitHub/ instead of GitHub API
    python scan-skills.py --local --csv skills-inventory.csv  # Export DataFrame to CSV

Requires: gh CLI authenticated (gh auth login)
"""

import subprocess
import json
import re
import sys
import os
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


def run_gh(args: List[str]) -> str:
    """Run a gh CLI command and return stdout."""
    result = subprocess.run(["gh"] + args, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  Warning: gh {' '.join(args[:3])}... failed: {result.stderr.strip()[:100]}")
        return ""
    return result.stdout.strip()


def list_repos(org: str = None, user: str = None) -> List[Dict]:
    """List repos from GitHub org or user."""
    repos = []
    if org:
        data = run_gh(["repo", "list", org, "--limit", "100", "--json", "name,url,isPrivate,updatedAt,description"])
        if data:
            repos.extend(json.loads(data))
    if user:
        data = run_gh(["repo", "list", user, "--limit", "100", "--json", "name,url,isPrivate,updatedAt,description"])
        if data:
            repos.extend(json.loads(data))
    return repos


def check_file_exists(owner: str, repo: str, path: str) -> Optional[Dict]:
    """Check if a file exists in a GitHub repo. Returns file info or None."""
    result = run_gh(["api", f"repos/{owner}/{repo}/contents/{path}", "--jq", ".name, .size, .html_url"])
    if result:
        lines = result.strip().split("\n")
        return {
            "name": lines[0] if len(lines) > 0 else path,
            "size": int(lines[1]) if len(lines) > 1 else 0,
            "url": lines[2] if len(lines) > 2 else "",
        }
    return None


def search_skills_in_repo(owner: str, repo: str) -> List[Dict]:
    """Search for SKILL.md files in a repo using GitHub API."""
    skills = []
    # Search for SKILL.md files
    result = run_gh([
        "api", f"search/code?q=filename:SKILL.md+repo:{owner}/{repo}",
        "--jq", ".items[] | .path"
    ])
    if result:
        for path in result.strip().split("\n"):
            if path:
                skills.append({"path": path, "repo": repo, "owner": owner})
    return skills


def scan_github(org: str = None, user: str = None) -> dict:
    """Scan GitHub repos for Claude Code artifacts."""
    inventory = {
        "scan_date": datetime.now().isoformat(),
        "scan_source": "github_api",
        "repos": [],
        "skills_summary": [],
    }

    repos = list_repos(org=org, user=user)
    print(f"Found {len(repos)} repos to scan\n")

    for repo_info in repos:
        repo_name = repo_info["name"]
        # Determine owner
        url = repo_info.get("url", "")
        if org and f"/{org}/" in url:
            owner = org
        elif user and f"/{user}/" in url:
            owner = user
        else:
            # Parse from URL
            parts = url.rstrip("/").split("/")
            owner = parts[-2] if len(parts) >= 2 else (org or user or "unknown")

        print(f"Scanning {owner}/{repo_name}...", end=" ")

        repo_entry = {
            "name": repo_name,
            "owner": owner,
            "url": url,
            "private": repo_info.get("isPrivate", False),
            "updated": repo_info.get("updatedAt", ""),
            "description": repo_info.get("description", ""),
            "has_claude_md": False,
            "has_agents_md": False,
            "skills": [],
        }

        # Check for CLAUDE.md
        claude_md = check_file_exists(owner, repo_name, "CLAUDE.md")
        if claude_md:
            repo_entry["has_claude_md"] = True

        # Check for AGENTS.md
        agents_md = check_file_exists(owner, repo_name, "AGENTS.md")
        if agents_md:
            repo_entry["has_agents_md"] = True

        # Search for skills
        skills = search_skills_in_repo(owner, repo_name)
        for skill in skills:
            repo_entry["skills"].append(skill["path"])
            inventory["skills_summary"].append({
                "repo": f"{owner}/{repo_name}",
                "path": skill["path"],
            })

        # Check common skill locations if search returned nothing
        if not skills:
            for skill_path in [".claude/skills", "skills"]:
                result = run_gh(["api", f"repos/{owner}/{repo_name}/contents/{skill_path}",
                                "--jq", ".[].name"])
                if result:
                    for folder in result.strip().split("\n"):
                        if folder:
                            skill_file = check_file_exists(owner, repo_name, f"{skill_path}/{folder}/SKILL.md")
                            if skill_file:
                                path = f"{skill_path}/{folder}/SKILL.md"
                                repo_entry["skills"].append(path)
                                inventory["skills_summary"].append({
                                    "repo": f"{owner}/{repo_name}",
                                    "path": path,
                                })

        markers = []
        if repo_entry["has_claude_md"]:
            markers.append("CLAUDE.md")
        if repo_entry["has_agents_md"]:
            markers.append("AGENTS.md")
        if repo_entry["skills"]:
            markers.append(f"{len(repo_entry['skills'])} skill(s)")

        print(", ".join(markers) if markers else "no AI artifacts")

        inventory["repos"].append(repo_entry)

    return inventory


def scan_local(base_path: str = None) -> dict:
    """Scan local filesystem for Claude Code artifacts."""
    if not base_path:
        base_path = os.path.expanduser("~/Documents/GitHub")

    inventory = {
        "scan_date": datetime.now().isoformat(),
        "scan_source": f"local:{base_path}",
        "repos": [],
        "skills_summary": [],
        "user_skills": [],
    }

    base = Path(base_path)
    print(f"Scanning {base}...\n")

    # Scan user-level skills
    user_skills_dir = Path.home() / ".claude" / "skills"
    if user_skills_dir.exists():
        print("=== User-level skills (~/.claude/skills/) ===")
        for skill_dir in sorted(user_skills_dir.iterdir()):
            if skill_dir.is_dir() or skill_dir.is_symlink():
                skill_file = skill_dir / "SKILL.md"
                if skill_file.exists():
                    is_symlink = skill_dir.is_symlink()
                    target = str(skill_dir.resolve()) if is_symlink else None
                    entry = {
                        "name": skill_dir.name,
                        "path": str(skill_file),
                        "symlink": is_symlink,
                        "target": target,
                    }
                    inventory["user_skills"].append(entry)
                    sym = f" -> {target}" if is_symlink else ""
                    print(f"  /{skill_dir.name}{sym}")
        print()

    # Walk through repos — handle nested structure (e.g., 04_PacerAI_GTM/website-PacerAI/)
    git_repos = set()
    for git_dir in base.rglob(".git"):
        if git_dir.is_dir() and "node_modules" not in str(git_dir) and ".venv" not in str(git_dir):
            git_repos.add(git_dir.parent)

    print(f"=== Repos found: {len(git_repos)} ===\n")

    for repo_path in sorted(git_repos):
        rel_path = repo_path.relative_to(base)
        repo_name = str(rel_path)

        repo_entry = {
            "name": repo_name,
            "path": str(repo_path),
            "has_claude_md": False,
            "has_agents_md": False,
            "skills": [],
        }

        # Check for CLAUDE.md
        if (repo_path / "CLAUDE.md").exists():
            repo_entry["has_claude_md"] = True

        # Check for AGENTS.md
        if (repo_path / "AGENTS.md").exists():
            repo_entry["has_agents_md"] = True

        # Search for SKILL.md files
        for skill_file in repo_path.rglob("SKILL.md"):
            # Skip node_modules, .venv, etc.
            skill_str = str(skill_file)
            if any(skip in skill_str for skip in ["node_modules", ".venv", "__pycache__"]):
                continue
            rel_skill = str(skill_file.relative_to(repo_path))
            repo_entry["skills"].append(rel_skill)
            inventory["skills_summary"].append({
                "repo": repo_name,
                "path": rel_skill,
            })

        markers = []
        if repo_entry["has_claude_md"]:
            markers.append("CLAUDE.md")
        if repo_entry["has_agents_md"]:
            markers.append("AGENTS.md")
        if repo_entry["skills"]:
            markers.append(f"{len(repo_entry['skills'])} skill(s)")

        if markers:
            print(f"  {repo_name}: {', '.join(markers)}")

        inventory["repos"].append(repo_entry)

    return inventory


def parse_skill_frontmatter(skill_path: str) -> Dict:
    """Parse YAML frontmatter from a SKILL.md file to extract name and description."""
    result = {"name": "", "description": ""}
    try:
        with open(skill_path, "r") as f:
            content = f.read()
        # Match YAML frontmatter between --- delimiters
        match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        if match:
            frontmatter = match.group(1)
            for line in frontmatter.split("\n"):
                if line.startswith("name:"):
                    result["name"] = line.split(":", 1)[1].strip()
                elif line.startswith("description:"):
                    result["description"] = line.split(":", 1)[1].strip()
    except (IOError, OSError):
        pass
    return result


def build_skills_dataframe(inventory: dict) -> "pandas.DataFrame":
    """Build a pandas DataFrame of all skills with timestamp, name, location, and description."""
    import pandas as pd

    scan_date = inventory["scan_date"]
    rows = []

    # User-level skills
    for skill in inventory.get("user_skills", []):
        skill_path = skill["path"]
        fm = parse_skill_frontmatter(skill_path)
        location = skill.get("target", str(Path(skill_path).parent)) if skill.get("symlink") else str(Path(skill_path).parent)
        # Shorten home dir for readability
        location = location.replace(os.path.expanduser("~"), "~")
        rows.append({
            "scan_date": scan_date,
            "skill": fm["name"] or skill["name"],
            "scope": "user",
            "location": location,
            "description": fm["description"],
        })

    # Repo-level skills
    for skill_info in inventory.get("skills_summary", []):
        repo_name = skill_info["repo"]
        skill_rel_path = skill_info["path"]

        # Try to resolve full path for local scans to read frontmatter
        description = ""
        skill_name = skill_rel_path.split("/")[-2] if "/" in skill_rel_path else skill_rel_path

        # Find the matching repo entry to get absolute path
        for repo in inventory.get("repos", []):
            if repo.get("name") == repo_name and repo.get("path"):
                full_path = os.path.join(repo["path"], skill_rel_path)
                fm = parse_skill_frontmatter(full_path)
                if fm["name"]:
                    skill_name = fm["name"]
                description = fm["description"]
                break

        location = f"{repo_name}/{skill_rel_path}"
        rows.append({
            "scan_date": scan_date,
            "skill": skill_name,
            "scope": "project",
            "location": location,
            "description": description,
        })

    df = pd.DataFrame(rows, columns=["scan_date", "skill", "scope", "location", "description"])
    return df


def print_summary(inventory: dict):
    """Print a formatted summary of the inventory."""
    print("\n" + "=" * 70)
    print("CLAUDE CODE SKILLS INVENTORY")
    print(f"Scanned: {inventory['scan_date'][:10]}")
    print(f"Source:  {inventory['scan_source']}")
    print("=" * 70)

    # User-level skills
    if inventory.get("user_skills"):
        print("\n## User-Level Skills (~/.claude/skills/)")
        print(f"{'Skill':<30} {'Symlink Target'}")
        print("-" * 70)
        for skill in inventory["user_skills"]:
            target = skill.get("target", "")
            if target:
                # Shorten the path for display
                target = target.replace(os.path.expanduser("~"), "~")
            sym = f"-> {target}" if skill.get("symlink") else "(local copy)"
            print(f"  /{skill['name']:<28} {sym}")

    # Skills found in repos
    if inventory["skills_summary"]:
        print(f"\n## Skills Found in Repos ({len(inventory['skills_summary'])} total)")
        print(f"{'Repo':<40} {'Skill Path'}")
        print("-" * 70)
        for skill in inventory["skills_summary"]:
            print(f"  {skill['repo']:<38} {skill['path']}")

    # AI-native readiness
    print("\n## AI-Native Readiness by Repo")
    print(f"{'Repo':<40} {'CLAUDE.md':<12} {'AGENTS.md':<12} {'Skills'}")
    print("-" * 70)
    for repo in sorted(inventory["repos"], key=lambda r: r["name"]):
        name = repo.get("name", repo.get("path", "?"))
        # Shorten long paths
        if len(name) > 38:
            name = "..." + name[-35:]
        claude = "yes" if repo["has_claude_md"] else "-"
        agents = "yes" if repo["has_agents_md"] else "-"
        skills = str(len(repo["skills"])) if repo["skills"] else "-"
        print(f"  {name:<38} {claude:<12} {agents:<12} {skills}")

    # Stats
    total_repos = len(inventory["repos"])
    with_claude = sum(1 for r in inventory["repos"] if r["has_claude_md"])
    with_agents = sum(1 for r in inventory["repos"] if r["has_agents_md"])
    with_skills = sum(1 for r in inventory["repos"] if r["skills"])
    total_skills = len(inventory["skills_summary"])

    print(f"\n## Summary")
    print(f"  Repos scanned:      {total_repos}")
    print(f"  With CLAUDE.md:     {with_claude}/{total_repos}")
    print(f"  With AGENTS.md:     {with_agents}/{total_repos}")
    print(f"  With skills:        {with_skills}/{total_repos}")
    print(f"  Total skills found: {total_skills}")
    if inventory.get("user_skills"):
        print(f"  User-level skills:  {len(inventory['user_skills'])}")


def main():
    parser = argparse.ArgumentParser(description="Scan repos for Claude Code skills inventory")
    parser.add_argument("--org", default=None, help="GitHub organization to scan")
    parser.add_argument("--user", default=None, help="GitHub user to scan")
    parser.add_argument("--local", action="store_true", help="Scan local filesystem instead of GitHub API")
    parser.add_argument("--path", default=None, help="Local base path (default: ~/Documents/GitHub)")
    parser.add_argument("--output", "-o", default=None, help="Save JSON output to file")
    parser.add_argument("--csv", default=None, help="Export skills DataFrame to CSV file")
    args = parser.parse_args()

    if args.local:
        inventory = scan_local(args.path)
    else:
        org = args.org or "PacerAI"
        user = args.user or "wsullivan-dev"
        if not args.org and not args.user:
            # Default: scan both
            inventory = scan_github(org=org, user=user)
        elif args.org:
            inventory = scan_github(org=org)
        else:
            inventory = scan_github(user=user)

    print_summary(inventory)

    # Build and display skills DataFrame
    try:
        df = build_skills_dataframe(inventory)
        if not df.empty:
            print("\n" + "=" * 70)
            print("SKILLS DATAFRAME")
            print("=" * 70)
            print(df.to_string(index=False))

            if args.csv:
                df.to_csv(args.csv, index=False)
                print(f"\nCSV saved to {args.csv}")
        else:
            print("\nNo skills found for DataFrame output.")
    except ImportError:
        if args.csv:
            print("\nWarning: pandas not installed. Cannot export CSV. Install with: pip install pandas")

    if args.output:
        with open(args.output, "w") as f:
            json.dump(inventory, f, indent=2)
        print(f"\nJSON saved to {args.output}")


if __name__ == "__main__":
    main()
