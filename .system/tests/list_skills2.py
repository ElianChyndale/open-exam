from pathlib import Path

skills = Path.home() / ".agents" / "skills"
for d in sorted(skills.iterdir()):
    if d.is_dir():
        sk = d / "SKILL.md"
        if sk.exists():
            lines = sk.read_text(encoding="utf-8", errors="replace").splitlines()
            # Find first non-frontmatter non-heading line
            in_frontmatter = False
            desc = ""
            for line in lines:
                s = line.strip()
                if s == "---":
                    in_frontmatter = not in_frontmatter
                    continue
                if in_frontmatter:
                    if s.startswith("description:") or s.startswith("Description:"):
                        desc = s.split(":", 1)[1].strip()[:80]
                    continue
                if not in_frontmatter and not desc:
                    if s and not s.startswith("#") and not s.startswith("```"):
                        desc = s[:80]
                        break
            # If still nothing, try the first non-empty line after frontmatter
            if not desc:
                for line in lines:
                    s = line.strip()
                    if s and s != "---" and not s.startswith("#"):
                        desc = s[:80]
                        break
            print(f"{d.name:35s} | {desc}")
