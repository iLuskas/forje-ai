---
name: forje-flow-feature
description: Implementa uma feature, bug fix ou refactor em um projeto pessoal — o usuário descreve a mudança direto ou aponta um arquivo de task. Use quando pedirem "adiciona", "cria", "implementa", "faz" algo em um projeto pessoal. Ciclo enxuto — clarificar → plano (quando vale a pena) → implementar nas convenções do repo → testar.
---

# Feature sem processo

Fluxo pessoal, sem card, sem aprovação de terceiros — só o suficiente pra não
codar às cegas nem quebrar o que já existe.

## Fluxo

1. **Entender o pedido** — texto livre, ou arquivo de task apontado: leia e use como
   descrição. Se faltar contexto essencial (qual módulo, comportamento esperado),
   pergunte antes de assumir.
2. **Carregar contexto — na ordem mais barata primeiro**:
   1. Existe `.claude/context.yaml`? Cruze a tarefa com o `covers` de cada doc e
      carregue **somente** os docs cujas áreas a mudança vai tocar — nunca o
      conjunto inteiro. Tarefa no módulo de pagamento não carrega doc de
      autenticação. Se o `covers` deixar dúvida entre dois docs, o `summary` de
      cada um (manifest v2) decide sem precisar abrir nenhum.
   2. Sem manifest: leia o `CLAUDE.md` do projeto se existir.
   3. Sem nenhum dos dois: olhada rápida na estrutura (linguagem, framework,
      testes) antes de decidir como implementar — e, ao fechar a tarefa, sugira
      `forje-ai:forje-docs-bootstrap` para a próxima sessão já começar barata.

   Em qualquer nível: se o projeto tiver um índice de código disponível
   (codegraph, graphify ou similar, via MCP), prefira consultá-lo a explorar
   arquivos crus — uma tool call no índice substitui um loop de grep/read.
3. **Plano — só quando a mudança não é óbvia** — se for trivial (ajuste pequeno,
   1-2 arquivos), pode ir direto pra implementação. Se envolver decisão de design,
   múltiplos arquivos, ou migração de dado, esboce o plano (arquivos afetados,
   abordagem, riscos) e confirme antes de escrever código. Se a decisão abrir
   várias ramificações dependentes entre si (a escolha de uma muda o resto do
   plano), use `forje-ai:forje-grilling` em vez de uma confirmação única.
4. **Implementar** seguindo as convenções que já existem no repo — nomenclatura,
   estrutura de pastas, estilo. Convenção do repo > preferência pessoal do momento.
5. **Testar** — caminho feliz + pelo menos um caso de erro, no framework que o repo
   já usa (ou o mais simples possível se o repo não tem framework de teste ainda).
6. **Fechar** — resuma o que mudou e como validar manualmente. Sugira
   `forje-ai:forje-code-review` antes de commitar algo mais sensível.

## Regras duras

- Com manifest presente, não carregue doc cujo `covers` não intersecta a mudança —
  a janela de contexto é orçamento, não estoque.
- Não invente convenção: se o repo não documenta um padrão, pergunte ou escolha o
  mais simples e diga que escolheu.
- Não implemente mudança grande/arriscada (migração, remoção de dado, mudança de
  schema) sem confirmar antes.
- Escopo extra no meio do caminho ("já aproveita e faz X") → sinalize que X é uma
  tarefa separada; não infla a entrega original.
