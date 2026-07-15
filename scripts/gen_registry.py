#!/usr/bin/env python3
"""Gera o bloco de tabela do forje-registry a partir dos frontmatters das skills.

A tabela entre os marcadores BEGIN/END GENERATED em
skills/forje-registry/SKILL.md é derivada automaticamente do `name` e
`description` de cada SKILL.md — fonte única de verdade, zero drift manual.

Uso:
    python scripts/gen_registry.py            # reescreve o bloco gerado
    python scripts/gen_registry.py --check    # falha (exit 1) se estiver defasado
"""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("requer PyYAML — rode `python -m pip install -r requirements.txt`")


def _safe_console() -> None:
    """Windows usa cp1252 por padrão; sem isso, qualquer char fora dela crasha o print."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


_safe_console()

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
REGISTRY = SKILLS_DIR / "forje-registry" / "SKILL.md"
BEGIN = "<!-- BEGIN GENERATED (scripts/gen_registry.py) — não edite à mão -->"
END = "<!-- END GENERATED -->"


def parse_frontmatter(skill_md: Path) -> dict:
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError(f"{skill_md}: sem frontmatter YAML")
    try:
        _, fm, _ = text.split("---", 2)
    except ValueError as exc:
        raise ValueError(f"{skill_md}: frontmatter mal delimitado") from exc
    data = yaml.safe_load(fm)
    if not isinstance(data, dict):
        raise ValueError(f"{skill_md}: frontmatter não é um mapa YAML")
    return data


def collect_skills() -> list[dict]:
    skills = []
    for d in sorted(SKILLS_DIR.iterdir()):
        if not d.is_dir() or d.name == "forje-registry":
            continue
        fm = parse_frontmatter(d / "SKILL.md")
        skills.append(fm)
    return skills


def render_table(skills: list[dict]) -> str:
    lines = [
        BEGIN,
        "",
        "| Invocar | O que faz / quando usar |",
        "|---------|--------------------------|",
    ]
    for fm in skills:
        desc = " ".join(str(fm["description"]).split()).replace("|", "\\|")
        lines.append(f"| `forje-ai:{fm['name']}` | {desc} |")
    lines += ["", END]
    return "\n".join(lines)


def main() -> int:
    check = "--check" in sys.argv
    content = REGISTRY.read_text(encoding="utf-8")

    if BEGIN not in content or END not in content:
        print(f"ERRO: marcadores GENERATED não encontrados em {REGISTRY}")
        return 1

    head, rest = content.split(BEGIN, 1)
    _, tail = rest.split(END, 1)
    try:
        skills = collect_skills()
    except Exception as exc:
        print(f"ERRO ao ler frontmatters: {exc}")
        return 1
    new_content = head + render_table(skills) + tail

    if new_content == content:
        print("registry: atualizado")
        return 0
    if check:
        print("registry: DEFASADO - rode `python scripts/gen_registry.py`")
        return 1
    REGISTRY.write_text(new_content, encoding="utf-8")
    print("registry: regenerado")
    return 0


if __name__ == "__main__":
    sys.exit(main())
