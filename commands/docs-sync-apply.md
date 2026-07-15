---
description: Corrige o drift dos docs vivos em escopo da tarefa atual (edita docs e manifest)
---
Invoque a skill `forje-ai:forje-docs-sync` em modo `--apply`.

Contrato deste comando: correções aplicadas diretamente nos docs, restritas ao
drift EM ESCOPO da tarefa/sessão atual; drift pré-existente achado de passagem
vira relatório, não edição. Ao final, atualize `synced_commit` (somente dos docs
conferidos) e `summary` quando a correção mudar o que o doc afirma.
