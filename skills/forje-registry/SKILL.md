---
name: forje-registry
description: Índice das minhas skills pessoais (Lucas Fernandes) para projetos pessoais. Use para decidir qual skill invocar para uma tarefa.
---

# forje-ai — Registry de skills

Skills pessoais disponíveis abaixo. Prefixo de invocação: `forje-ai:`.

## Skills

| Invocar | Gatilho | O que faz |
|---------|---------|-----------|
| `forje-ai:forje-flow-feature` | "adiciona", "cria", "implementa", "faz" algo num projeto pessoal | Ciclo enxuto: clarificar → plano (quando vale a pena) → implementar nas convenções do repo → testar |
| `forje-ai:forje-code-review` | "revisa", "review", "confere meu código" | Revisão do diff — correção, simplicidade, segurança básica. Somente leitura |
| `forje-ai:forje-docs-sync` | Início de tarefa que planeja a partir de docs vivos; fim de implementação; "os docs estão desatualizados" | Detecta drift entre `.claude/context.yaml` e o código; `--report` ou `--apply` |
| `forje-ai:forje-docs-bootstrap` | Projeto sem docs vivos: "gera os contexts", "documenta esse projeto" | Detecta o perfil do projeto e gera o conjunto de docs adequado + `.claude/context.yaml` |
| `forje-ai:forje-grilling` | "me grilla sobre X", "quero stress-testar essa decisão antes de codar" | Entrevista uma pergunta por vez, com recomendação, até entendimento compartilhado |
| `forje-ai:forje-skill-authoring` | "cria uma skill", "nova skill", editar skill existente | Convenções de nomenclatura e estrutura para skills deste plugin |

## Como escolher

- Feature/bug/refactor pedido direto → `forje-flow-feature`
- "revisa meu código / o diff" → `forje-code-review`
- "docs desatualizados / confere docs vs código" → `forje-docs-sync`
- Projeto ainda sem docs de contexto → `forje-docs-bootstrap`
- Stress-testar uma decisão/plano/ideia antes de agir → `forje-grilling`
- Criar/editar skill deste plugin → `forje-skill-authoring`
