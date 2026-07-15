---
name: forje-docs-sync
description: Motor de sincronização de documentação viva para projetos pessoais. Detecta divergências entre os docs declarados no .claude/context.yaml do repositório e o código atual, e reporta (--report) ou corrige (--apply). Use no início de uma tarefa que vá planejar a partir de docs vivos, ao final de uma implementação que muda comportamento documentado, ou quando suspeitar que os docs estão desatualizados.
---

# Docs Sync (documentação viva)

Doc de contexto descreve o código no momento em que foi escrito e apodrece a cada
commit. Esta skill compara os docs vivos declarados pelo repo com o código atual e
elimina o drift — lendo o mínimo possível: metadados antes de docs, diff antes de
auditoria.

## Pré-requisito — manifest (schema v2)

O repositório declara seus docs vivos em `.claude/context.yaml`:

```yaml
version: 2
docs:
  - path: docs/architecture.md
    covers: [src/api, src/core]
    summary: "Camadas API→Service→Repo; integrações Stripe e R2; fila via outbox"
    synced_commit: a1b2c3d   # último commit em que este doc foi conferido; null = nunca
  - path: docs/business-rules.md
    covers: [src/domain]
    summary: "Regras de pedido: expiração 30d, limites por plano, cálculo de multa"
    synced_commit: a1b2c3d
```

- `summary` — 1 linha (~20 tokens) dizendo o que o doc afirma. É o que permite a
  outras skills decidir relevância **sem abrir o doc**.
- `synced_commit` é **por doc**: docs de área fria não são re-checados porque uma
  área quente mudou. Consequência aceita: docs podem estar em "épocas" diferentes.

**Sem manifest:** informe que o repo ainda não aderiu ao padrão e ofereça rodar
`forje-ai:forje-docs-bootstrap`; não invente uma lista de docs.

**Manifest sem `version` (legado v1):** trate `sync.last_synced_commit` global como
seed do `synced_commit` de cada doc. Em `--report`, apenas avise que o manifest é
v1. Em `--apply`, migre para v2 (gere `summary` a partir da leitura de cada doc já
feita na sessão) e registre a migração no relatório final.

## Modos

| Modo | Quando | Comportamento |
|------|--------|---------------|
| `--report` | Antes de planejar a partir dos docs; drift achado de passagem | Lista divergências com evidência (`arquivo:linha` vs. trecho do doc). Não edita nada. |
| `--apply` | Fim de uma implementação, para registrar o que mudou | Corrige os docs diretamente, sem pedir confirmação extra |

`--apply` só toca em drift **em escopo** da tarefa atual. Drift pré-existente achado
de passagem vira relatório para decisão manual.

## Fluxo

1. **Ler o manifest** — schema, docs, `covers`, `synced_commit` por doc.
2. **Validar cada marcador** — `git cat-file -e <hash>^{commit}`. Hash que não
   existe mais (rebase, squash, força-push) = marcador ausente; fallback:
   `git log -1 --format=%H -- <doc>`.
3. **Delimitar o diff por doc** — `git log --oneline <synced_commit>..HEAD --
   <covers>`. Diff vazio: doc está em dia, **não abra nem o doc nem o código**.
   Só faça auditoria integral (sem diff, claim por claim) se pedido
   explicitamente — é caro e sujeito a falso positivo.
4. **Comparar por doc com diff** — confronte as afirmações do doc com o código
   atual lido agora. Claims com âncora `(arquivo)` verificam-se abrindo o arquivo
   apontado; claims sem âncora exigem busca — ao corrigi-las em `--apply`,
   adicione a âncora para baratear o próximo sync.
5. **Classificar** — `desatualizado` (doc afirma algo que o código não faz mais),
   `lacuna` (código novo sem doc), `erro` (doc nunca esteve certo).
6. **Agir conforme o modo** — reportar em tabela (doc, seção, divergência,
   evidência) ou aplicar as correções preservando estilo/estrutura do doc.
7. **Atualizar metadados** — só em `--apply`: `synced_commit` ← HEAD **apenas dos
   docs conferidos nesta sessão**; se a correção mudou o que o doc afirma,
   atualize o `summary` na mesma passada.

## Regras duras

- Nunca edite docs nem manifest em modo `--report`.
- Divergência sem evidência em código (`arquivo:linha`) não é divergência, é
  palpite — não reporte.
- Doc coberto pelo manifest que não existe mais: reporte como erro de manifest,
  não recrie por conta própria.
- `synced_commit` só avança para docs efetivamente conferidos — nunca em lote.
- `summary` desatualizado é drift de metadado: corrija junto com o doc.
