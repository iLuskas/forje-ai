---
name: forje-skill-authoring
description: Convenções para criar ou editar skills pessoais neste plugin (forje-*). Use quando o Lucas pedir para criar, alterar ou padronizar uma skill pessoal.
---

# Autoria de skills — forje-ai

Skill boa é a que dá pra invocar sem reler o código-fonte dela. Estas convenções
mantêm as skills pessoais previsíveis e fáceis de manter — versão enxuta do
processo, sem aparato de compliance.

## Estrutura

```
skills/forje-{acao}/
  SKILL.md            # ideal ≤ 150 linhas
  references/         # opcional — detalhe carregado sob demanda
    <slug>.md
```

`SKILL.md` contém, nesta ordem:

1. **Frontmatter** — `name` (igual ao diretório) e `description` (1-2 frases: o
   que faz + quando usar, com gatilhos concretos — é o texto que decide a
   invocação).
2. **Parágrafo de abertura** — o problema que a skill resolve.
3. **Fluxo** — passos numerados e diretos.
4. **Regras duras** (opcional, se houver algo que nunca deve acontecer).

Detalhe extenso vai para `references/` — não infle o corpo principal do
`SKILL.md`.

## Checklist antes de terminar

- [ ] Nome segue `forje-{acao}`; diretório == `name` do frontmatter.
- [ ] Frontmatter é YAML válido — cuidado com `: ` sem aspas dentro da
      `description`, que quebra o parser. Use `—` no lugar ou envolva em aspas.
- [ ] `description` responde "quando invocar?" sem precisar abrir o corpo.
- [ ] Registrada na tabela de `skills/forje-registry/SKILL.md`.
- [ ] Se mudou algo distribuído, bump de versão em `.claude-plugin/plugin.json`
      e `marketplace.json` (mesmo número).
- [ ] Não duplica skill existente — gatilho colidindo, edite a existente.

## Regras duras

- Nunca registre no registry uma skill que ainda não existe.
