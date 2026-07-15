#!/usr/bin/env python3
"""Valida a integridade do plugin forje-ai. Exit 0 = tudo ok.

Checa (cada item elimina uma classe de falha silenciosa):
  1. Todo skills/<dir>/SKILL.md tem frontmatter YAML válido com name+description
     (frontmatter quebrado faz a skill sumir do picker sem erro).
  2. `name` do frontmatter == nome do diretório.
  3. Versão de .claude-plugin/plugin.json == marketplace.json (duplicação mantida
     à mão nos dois arquivos).
  4. Bloco gerado do forje-registry está em dia (delega a gen_registry.py --check).

Uso: python scripts/validate.py
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
errors: list[str] = []


def check_frontmatters() -> None:
    for d in sorted(SKILLS_DIR.iterdir()):
        if not d.is_dir():
            continue
        skill_md = d / "SKILL.md"
        if not skill_md.exists():
            errors.append(f"{d.name}: sem SKILL.md")
            continue
        text = skill_md.read_text(encoding="utf-8")
        if not text.startswith("---"):
            errors.append(f"{d.name}: SKILL.md sem frontmatter YAML")
            continue
        try:
            _, fm_raw, _ = text.split("---", 2)
            fm = yaml.safe_load(fm_raw)
        except Exception as exc:  # YAML inválido = skill some silenciosamente
            errors.append(f"{d.name}: frontmatter YAML inválido — {exc}")
            continue
        if not isinstance(fm, dict):
            errors.append(f"{d.name}: frontmatter não é um mapa YAML")
            continue
        for field in ("name", "description"):
            if not fm.get(field):
                errors.append(f"{d.name}: frontmatter sem `{field}`")
        if fm.get("name") and fm["name"] != d.name:
            errors.append(
                f"{d.name}: frontmatter name=`{fm['name']}` != diretório `{d.name}`"
            )


def check_versions() -> None:
    plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text("utf-8"))
    market = json.loads(
        (ROOT / ".claude-plugin" / "marketplace.json").read_text("utf-8")
    )
    p_ver = plugin.get("version")
    m_vers = {p.get("version") for p in market.get("plugins", [])}
    if not p_ver:
        errors.append("plugin.json: sem `version`")
    elif m_vers != {p_ver}:
        errors.append(
            f"versões divergem: plugin.json={p_ver} vs marketplace.json={m_vers}"
        )


def check_registry() -> None:
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "gen_registry.py"), "--check"],
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        errors.append(f"registry defasado: {r.stdout.strip() or r.stderr.strip()}")


def main() -> int:
    check_frontmatters()
    check_versions()
    check_registry()
    if errors:
        print("FALHOU:")
        for e in errors:
            print(f"  ✗ {e}")
        return 1
    print("validate: tudo ok ✓")
    return 0


if __name__ == "__main__":
    sys.exit(main())
