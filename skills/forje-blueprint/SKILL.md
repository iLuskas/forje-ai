---
name: forje-blueprint
description: Gera docs vivos e .claude/context.yaml a partir da INTENÇÃO em projetos novos ou vazios — um prompt de visão, um .md de requisitos, um PDF de spec. Direção inversa do forje-docs-bootstrap (que extrai do código existente). Use quando o repositório está vazio ou embrionário mas existe material de visão/spec na conversa ou em arquivo.
---

# Blueprint (o risco da lâmina)

O bootstrap faz arqueologia: destila docs de código que existe. Esta skill faz o
risco: destila docs da intenção, antes de existir metal. O produto é o mesmo —
docs vivos + manifest v2 — para que o resto da forja funcione sem saber a origem.

## Fluxo

1. **Reunir a fonte** — o material de visão pode ser prompt na conversa, `.md`,
   PDF ou mistura. Se algo relevante só existe na conversa, **persista primeiro**
   em `docs/vision.md` (conversa morre com a janela; âncora precisa de alvo
   durável). PDF: referencie o arquivo ou extraia o essencial para `.md`.

2. **Provar no fogo antes de riscar** — se a visão tem ambiguidade estrutural ou
   decisões grandes em aberto (stack? modelo de dados? monolito/serviços?),
   sugira `forje-ai:forje-grilling` sobre a visão ANTES de gerar docs. Riscar em
   cima de decisão não tomada produz doc que nasce morto.

3. **Gerar os docs** — mesmos artefatos e estilo do bootstrap (densidade, não
   taquigrafia; claims diretas), com uma diferença: as âncoras são **tipadas de
   spec** — `"pedidos expiram em 30 dias (spec: docs/vision.md)"`. Isso marca a
   claim como intenção, não fato verificado em código:
   - `project-context.md` — o que é, pra quem, escopo do MVP.
   - `architecture.md` — a arquitetura *pretendida*: stack, camadas, integrações.
   - `business-rules.md` — regras extraídas da spec, cada uma com âncora `spec:`.
   O que a spec não diz, não existe: incerteza vira seção `## Aberto` explícita,
   nunca decisão inventada.

4. **Criar `.claude/context.yaml`** (schema v2) — `covers` aponta para os
   diretórios *planejados* na arquitetura (ainda inexistentes; o sync e o hook
   lidam bem com paths vazios). `summary` de 1 linha por doc.

5. **Gravar o risco no metal** — termine commitando docs + manifest (sugira ao
   usuário se não puder) e grave esse hash como `synced_commit` de cada doc.
   Repo sem nenhum commit ainda: este commit inicial resolve; nunca deixe
   `synced_commit` sem valor válido, ou a sentinela avisará toda sessão.

## Ciclo de vida das âncoras (spec → código)

A claim nasce `(spec: ...)` e migra para `(src/...)` conforme vira realidade —
essa migração é feita pelo `forje-docs-sync`, não por esta skill. O doc começa
desenho e termina lâmina.

## Regras duras

- Não invente requisito, regra ou decisão ausente da fonte — incerteza é
  registrada como aberta, não resolvida por conta própria.
- Não gere código nem estrutura de diretórios: o risco é desenho, não martelo.
  Implementação é com `forje-ai:forje-flow-feature`.
- Toda claim tem âncora `spec:` apontando para fonte persistida no repo — nunca
  para "a conversa".
- Repo com código relevante já existente não é caso desta skill: use
  `forje-ai:forje-docs-bootstrap` (ou os dois, se há código E spec nova, cada um
  na sua metade).
