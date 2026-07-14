# forje-ai

Plugin **pessoal** de Claude Code do Lucas Fernandes — para uso nos meus projetos
fora da Tasken. Sem regras de compliance, LGPD ou processo corporativo: é só o meu
jeito de trabalhar, meus atalhos e minhas preferências.

Instale como plugin local (marketplace apontando para este diretório) em qualquer
projeto pessoal onde eu queira essas skills disponíveis.

## Estrutura

```
forje-ai/
├── .claude-plugin/        # plugin.json + marketplace.json
├── skills/
│   └── forje-registry/    # índice das minhas skills — injetado via SessionStart
└── README.md
```

## Como adicionar uma skill nova

1. Crie `skills/<nome>/SKILL.md` com frontmatter `name` + `description`.
2. Liste a skill na tabela em `skills/forje-registry/SKILL.md`.
3. Se mudar algo distribuído (skill, hook, doc), suba a versão em
   `.claude-plugin/plugin.json` e `.claude-plugin/marketplace.json` (mesmo número).
