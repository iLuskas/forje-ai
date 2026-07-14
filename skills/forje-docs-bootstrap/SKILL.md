---
name: forje-docs-bootstrap
description: Gera do zero os docs vivos de um projeto pessoal que ainda não tem documentação de contexto — detecta o perfil (API/backend .NET, Node, Python, frontend React) e gera o conjunto de docs adequado, terminando com o .claude/context.yaml criado. Use quando o Lucas pedir "gera os contexts", "documenta esse projeto", "cria o context.md", ou quando um projeto pessoal sem docs vivos precisar aderir ao padrão.
---

# Docs Bootstrap (gerar documentação viva do zero)

O `forje-ai:forje-docs-sync` mantém docs que já existem; esta skill resolve o passo
anterior — projeto sem nenhum doc de contexto. Detecta o perfil, gera os docs um por
vez (cada um com leitura dedicada do código) e deixa o repo pronto para manutenção
automática.

## Fluxo

1. **Detectar o perfil** — inspecione o repositório, não pergunte o que dá pra
   descobrir sozinho:

   | Evidência | Perfil | Docs a gerar |
   |-----------|--------|--------------|
   | `.csproj` (API/worker .NET) | Backend .NET | `context.md`, `architecture.md`, `project-structure.md`, `coding-standards.md` |
   | `package.json` com `express`/`nest`/`fastify`/`koa` | Backend Node | mesmo conjunto acima |
   | `pyproject.toml` / `requirements.txt` | Python (API, worker, CLI) | mesmo conjunto acima |
   | `package.json` com `react`/`next`/`vite` | Frontend | `frontend-context.md`, `project-structure.md`, `user-interactions.md` |

   Caso ambíguo (fullstack, monorepo): mostre o que detectou e pergunte qual perfil
   (ou combinação) aplicar.

2. **Confirmar o plano** antes de gerar — liste os docs, a ordem e o que ficou de
   fora. Doc que já existe **não é regenerado**: aponte o `forje-docs-sync` para ele
   e gere só os que faltam.

3. **Gerar um doc por vez**, nesta ordem: `project-structure` → `context` →
   `architecture`/`frontend-context` → `coding-standards`/`user-interactions` (o
   mais difícil por último, com a base já mapeada). Para cada doc, leia o código de
   verdade seção por seção — não gere dois docs numa mesma passada rasa. Conteúdo
   mínimo de cada um:
   - `project-structure.md` — árvore de pastas relevante e o papel de cada uma.
   - `context.md` / `frontend-context.md` — o que o sistema faz, principais fluxos,
     stack e como rodar localmente.
   - `architecture.md` — camadas, fluxo de dados, integrações externas.
   - `coding-standards.md` — convenções que o próprio código já revela (nomenclatura,
     tratamento de erro, padrão de teste).
   - `user-interactions.md` — telas/fluxos principais e o que o usuário faz em cada
     um (só no perfil frontend).

4. **Consolidar pendências** — liste em um bloco único tudo marcado como
   "Necessita validação".

5. **Criar `.claude/context.yaml`** com um item por doc gerado, `covers` apontando
   para os diretórios reais que cada um descreve (estreito é melhor que largo) —
   formato completo em `forje-ai:forje-docs-sync`. `sync.last_synced_commit: null`.

6. **`CLAUDE.md` enxuto** — se o repo não tiver, ofereça criar: resumo do projeto,
   ponteiros pros docs gerados, e a regra de manutenção (`--report`/`--apply`).

## Regras duras

- Nunca invente informação: toda afirmação deriva de código lido nesta sessão;
  incerteza vira "Necessita validação", não prosa confiante.
- Doc existente não é sobrescrito nem "melhorado" de passagem — isso é escopo do
  `forje-docs-sync`.
- Um doc por passada de análise; não gere o conjunto inteiro de uma vez.
