from pathlib import Path

skills = Path.home() / ".agents" / "skills"
for d in sorted(skills.iterdir()):
    if d.is_dir():
        sk = d / "SKILL.md"
        if sk.exists():
            lines = sk.read_text(encoding="utf-8", errors="replace").splitlines()
            desc = ""
            for line in lines[:20]:
                s = line.strip()
                if s.startswith(">") or s.startswith("Description"):
                    desc = s[:80]
                    break
            if not desc:
                for line in lines[:5]:
                    s = line.strip()
                    if s and not s.startswith("#"):
                        desc = s[:80]
                        break
            print(f"{d.name:35s} | {desc}")
