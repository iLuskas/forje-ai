---
name: forje-docs-sync
description: Motor de sincronização de documentação viva para projetos pessoais. Detecta divergências entre os docs declarados no .claude/context.yaml do repositório e o código atual, e reporta (--report) ou corrige (--apply). Use no início de uma tarefa que vá planejar a partir de docs vivos, ao final de uma implementação que muda comportamento documentado, ou quando suspeitar que os docs estão desatualizados.
---

# Docs Sync (documentação viva)

Doc de contexto descreve o código no momento em que foi escrito e apodrece a cada
commit. Esta skill compara os docs vivos declarados pelo repo com o código atual e
elimina o drift.

## Pré-requisito — manifest

O repositório declara seus docs vivos em `.claude/context.yaml`:

```yaml
docs:
  - path: docs/architecture.md
    covers: [src/api, src/core]
  - path: docs/business-rules.md
    covers: [src/domain]
sync:
  last_synced_commit: <hash ou null>
```

Sem manifest: informe que o repo ainda não aderiu ao padrão e ofereça rodar
`forje-ai:forje-docs-bootstrap`; não invente uma lista de docs.

## Modos

| Modo | Quando | Comportamento |
|------|--------|---------------|
| `--report` | Antes de planejar a partir dos docs; drift achado de passagem | Lista divergências com evidência (`arquivo:linha` vs. trecho do doc). Não edita nada. |
| `--apply` | Fim de uma implementação, para registrar o que mudou | Corrige os docs diretamente, sem pedir confirmação extra |

`--apply` só toca em drift **em escopo** da tarefa atual. Drift pré-existente achado
de passagem vira relatório para decisão manual.

## Fluxo

1. **Ler o manifest** — lista de docs, áreas cobertas, `sync.last_synced_commit`.
2. **Delimitar o diff** — `git log --oneline <last_synced_commit>..HEAD -- <áreas>` +
   `git diff --stat`. Sem marcador, use `git log -1 --format=%H -- <doc>` por doc.
   Diff vazio nas áreas cobertas: diga isso e pare — só faça auditoria integral
   (sem diff, claim por claim) se pedido explicitamente, é caro e sujeito a falso
   positivo.
3. **Comparar por doc** — confronte as afirmações do doc com o código atual lido
   agora, não com memória da base.
4. **Classificar** — `desatualizado` (doc afirma algo que o código não faz mais),
   `lacuna` (código novo sem doc), `erro` (doc nunca esteve certo).
5. **Agir conforme o modo** — reportar em tabela (doc, seção, divergência,
   evidência) ou aplicar as correções preservando estilo/estrutura do doc original.
6. **Atualizar o marcador** (`sync.last_synced_commit` ← HEAD) — só em `--apply`.

## Regras duras

- Nunca edite docs em modo `--report`.
- Divergência sem evidência em código (`arquivo:linha`) não é divergência, é
  palpite — não reporte.
- Doc coberto pelo manifest que não existe mais: reporte como erro de manifest, não
  recrie por conta própria.
