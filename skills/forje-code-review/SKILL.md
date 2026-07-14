---
name: forje-code-review
description: Revisão de código para projetos pessoais — correção, aderência às convenções do repositório, simplicidade e segurança básica — sobre o diff atual. Somente leitura. Use quando o Lucas pedir "revisa", "review", "confere meu código", ou antes de commitar/abrir PR num projeto pessoal.
---

# Code Review pessoal

Revisão direta ao ponto: bugs, complexidade desnecessária e os erros de segurança
mais comuns — sem checklist corporativo.

## Escopo do diff

Nesta ordem: o que o Lucas apontar; senão `git diff` (staged + unstaged); senão
`git diff <branch-base>...HEAD`.

## Fluxo

1. Leia o diff inteiro; para cada arquivo tocado, leia o suficiente do entorno pra
   julgar o contexto — não revise linha isolada.
2. Aplique o checklist abaixo; para cada achado, cite `arquivo:linha`, explique o
   defeito e proponha a correção.
3. Classifique: **bloqueante** (bug, falha de segurança) / **importante** (padrão
   quebrado, teste faltando) / **sugestão**.
4. Entregue o veredito final: pronto pra commitar ou não, e por quê.

## Checklist

**Correção**
- O código faz o que deveria? Caminhos de erro tratados?
- Estados assíncronos (loading/erro/sucesso) cobertos? Race conditions?

**Simplicidade**
- Abstração além do que a tarefa pede? Três linhas repetidas são melhores que uma
  abstração prematura.
- Código morto, comentário óbvio, `TODO` esquecido.

**Segurança básica (bloqueantes)**
- Segredo hardcoded (chave, token, senha, URL com credencial).
- Injeção (SQL, comando, path traversal) por concatenar entrada do usuário sem
  sanitização.
- Dependência nova sem necessidade clara.

## Regras duras

- Review é **somente leitura**: não corrija o código durante a revisão, proponha.
- Cada achado tem `arquivo:linha` — sem apontamento vago.
- Bloqueante aberto = não está pronto, mesmo que o resto esteja bom.
