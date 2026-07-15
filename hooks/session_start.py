#!/usr/bin/env python3
"""SessionStart hook do forje-ai — sentinela de drift de docs vivos.

Contrato (nesta ordem de prioridade):
  1. NUNCA quebrar o início da sessão: qualquer erro interno = exit 0 silencioso.
  2. Sessão limpa (sem manifest, ou sem drift) = ZERO output, zero tokens.
  3. Com drift potencial: uma linha compacta por doc (máx. 3) + call to action.

Custo: só computação local (git), nenhum token gasto pra detectar — o LLM só
paga pelos ~20-60 tokens do aviso, e só quando há o que avisar.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

MAX_DOCS_LISTED = 3

def _safe_console() -> None:
    """Windows usa cp1252 por padrão; sem isso, qualquer char fora dela crasha o print."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


_safe_console()



def git(*args: str) -> str | None:
    """Roda git no cwd; None em qualquer falha."""
    try:
        r = subprocess.run(
            ["git", *args], capture_output=True, text=True, timeout=10
        )
        return r.stdout.strip() if r.returncode == 0 else None
    except Exception:
        return None


def load_manifest() -> dict | None:
    path = Path(".claude/context.yaml")
    if not path.is_file():
        return None
    try:
        import yaml  # import tardio: sem pyyaml na máquina = silêncio, não crash

        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else None
    except Exception:
        return None


def commit_exists(hash_: str) -> bool:
    return git("cat-file", "-e", f"{hash_}^{{commit}}") is not None


def drift_for(doc: dict, fallback_marker: str | None) -> str | None:
    """Retorna a linha de aviso do doc, ou None se está em dia."""
    path = doc.get("path", "?")
    covers = doc.get("covers") or []
    marker = doc.get("synced_commit") or fallback_marker

    if marker and not commit_exists(str(marker)):
        marker = None  # rebase/squash: marcador aponta pra commit que não existe

    if not marker:
        return f"{path}: sem marcador de sync válido"

    count = git("rev-list", "--count", f"{marker}..HEAD", "--", *map(str, covers))
    if count is None or count == "0":
        return None
    areas = ", ".join(map(str, covers)) or "(covers vazio)"
    return f"{path}: {count} commit(s) em {areas} desde o último sync"


def main() -> int:
    manifest = load_manifest()
    if not manifest or not git("rev-parse", "--git-dir"):
        return 0  # sem manifest ou fora de repo git: silêncio

    docs = manifest.get("docs") or []
    is_v1 = "version" not in manifest
    fallback = (manifest.get("sync") or {}).get("last_synced_commit") if is_v1 else None

    warnings = [w for d in docs if isinstance(d, dict) if (w := drift_for(d, fallback))]
    if not warnings:
        return 0  # tudo em dia: zero tokens injetados

    shown = warnings[:MAX_DOCS_LISTED]
    extra = len(warnings) - len(shown)
    lines = ["[forje-ai] docs vivos possivelmente defasados:"]
    lines += [f"  - {w}" for w in shown]
    if extra > 0:
        lines.append(f"  - (+{extra} outro(s) doc(s))")
    if is_v1:
        lines.append("  manifest v1 detectado - `forje-docs-sync --apply` migra pra v2")
    lines.append("Rode `forje-ai:forje-docs-sync --report` antes de planejar em cima dos docs.")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)  # contrato nº 1: hook nunca derruba a sessão
