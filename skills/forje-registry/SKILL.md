---
name: forje-registry
description: Índice das minhas skills pessoais para projetos pessoais. Use para decidir qual skill invocar para uma tarefa.
---

# forje-ai — Registry de skills

Skills pessoais disponíveis abaixo. Prefixo de invocação: `forje-ai:`.

## Skills

<!-- BEGIN GENERATED (scripts/gen_registry.py) — não edite à mão -->

| Invocar | O que faz / quando usar |
|---------|--------------------------|
| `forje-ai:forje-code-review` | Revisão de código para projetos pessoais — correção, aderência às convenções do repositório, simplicidade e segurança básica — sobre o diff atual. Somente leitura. Use quando pedirem "revisa", "review", "confere meu código", ou antes de commitar/abrir PR num projeto pessoal. |
| `forje-ai:forje-docs-bootstrap` | Gera do zero os docs vivos de um projeto pessoal que ainda não tem documentação de contexto — detecta o perfil (API/backend .NET, Node, Python, frontend React) e gera o conjunto de docs adequado, terminando com o .claude/context.yaml criado. Use quando pedirem "gera os contexts", "documenta esse projeto", "cria o context.md", ou quando um projeto pessoal sem docs vivos precisar aderir ao padrão. |
| `forje-ai:forje-docs-sync` | Motor de sincronização de documentação viva para projetos pessoais. Detecta divergências entre os docs declarados no .claude/context.yaml do repositório e o código atual, e reporta (--report) ou corrige (--apply). Use no início de uma tarefa que vá planejar a partir de docs vivos, ao final de uma implementação que muda comportamento documentado, ou quando suspeitar que os docs estão desatualizados. |
| `forje-ai:forje-flow-feature` | Implementa uma feature, bug fix ou refactor em um projeto pessoal — o usuário descreve a mudança direto ou aponta um arquivo de task. Use quando pedirem "adiciona", "cria", "implementa", "faz" algo em um projeto pessoal. Ciclo enxuto — clarificar → plano (quando vale a pena) → implementar nas convenções do repo → testar. |
| `forje-ai:forje-grilling` | Interroga o usuário sobre um plano, decisão ou ideia até alcançar entendimento compartilhado — uma pergunta por vez, sempre com uma recomendação, sem agir até confirmação explícita. Use quando pedirem para "stress-testar" uma decisão, disserem "me grilla sobre X", "quero validar essa ideia antes de codar", ou quando outra skill deste plugin encontrar uma decisão não-trivial no passo de clarificação. |
| `forje-ai:forje-skill-authoring` | Convenções para criar ou editar skills pessoais neste plugin (forje-*). Use quando pedirem para criar, alterar ou padronizar uma skill pessoal. |

<!-- END GENERATED -->

## Como escolher

- Feature/bug/refactor pedido direto → `forje-flow-feature`
- "revisa meu código / o diff" → `forje-code-review`
- "docs desatualizados / confere docs vs código" → `forje-docs-sync`
- Projeto ainda sem docs de contexto → `forje-docs-bootstrap`
- Stress-testar uma decisão/plano/ideia antes de agir → `forje-grilling`
- Criar/editar skill deste plugin → `forje-skill-authoring`
