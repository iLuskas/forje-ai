# forje-ai

🇧🇷 Português | [🇺🇸 English](./README.en.md)

> Plugin pessoal de skills para o [Claude Code](https://claude.com/claude-code) — meu jeito de trabalhar em projetos pessoais, empacotado para eu levar de repo em repo (e emprestar pra quem quiser).

Isso não carrega nenhuma regra de compliance, LGPD ou processo corporativo —
é feito pra projeto pessoal: sem card, sem aprovação de terceiros, sem
checklist de auditoria. Uso livre: sinta-se à vontade pra clonar, alterar e
distribuir.

## Sumário

- [O que é isso](#o-que-é-isso)
- [Como funciona](#como-funciona)
- [Instalação](#instalação)
- [Como testar](#como-testar)
- [Como usar no dia a dia](#como-usar-no-dia-a-dia)
- [As skills](#as-skills)
- [Por que "docs vivos" economiza token (e tempo)](#por-que-docs-vivos-economiza-token-e-tempo)
- [Estrutura do repo](#estrutura-do-repo)
- [Como adicionar uma skill nova](#como-adicionar-uma-skill-nova)
- [Roadmap / ideias futuras](#roadmap--ideias-futuras)
- [Licença](#licença)

## O que é isso

Um **plugin de Claude Code**: um pacote de `skills` (arquivos `SKILL.md` com
instruções em linguagem natural) que o Claude Code carrega automaticamente
quando você tem o plugin habilitado. Cada skill ensina o Claude a conduzir um
tipo de tarefa do jeito que eu prefiro — implementar uma feature, revisar
código, manter documentação de contexto atualizada, ou me interrogar antes de
eu tomar uma decisão precipitada.

A ideia central: meus projetos pessoais são pequenos, não têm Jira, não têm
outro dev revisando comigo — mas ainda me beneficio do mesmo rigor de
"planeja antes de codar" e "documentação que se mantém sozinha" que uso no
trabalho. Este plugin é esse rigor, sem o aparato corporativo em volta.

## Como funciona

Um plugin de Claude Code é só uma pasta com um manifesto e uma coleção de
skills:

```
forje-ai/
├── .claude-plugin/
│   ├── plugin.json        # nome, versão, descrição do plugin
│   └── marketplace.json   # como o Claude Code descobre/instala este plugin
└── skills/
    └── <nome-da-skill>/
        └── SKILL.md        # frontmatter (name + description) + instruções
```

Quando o plugin está habilitado numa sessão, o Claude Code lê o `name` e a
`description` de cada `SKILL.md` (sem carregar o corpo inteiro) e usa isso
para decidir, pelo seu pedido em linguagem natural, qual skill invocar — não
existe palavra-chave mágica nem comando decorado. Pedir "revisa esse código
pra mim" já é o suficiente para o Claude reconhecer que a `forje-code-review`
se aplica e carregar o conteúdo completo dela só nesse momento.

Uma coisa que este plugin **não** faz: forçar a leitura do índice de skills
em toda sessão via hook de `SessionStart`. `forje-registry` é só mais uma
skill; o Claude a invoca quando faz sentido
(por exemplo, se você perguntar "quais skills eu tenho disponíveis aqui?").
Isso é proposital: mantém o plugin simples e sem custo de token fixo por
sessão. Se um dia eu quiser essa garantia, é questão de adicionar um
`hooks/hooks.json` — ver [Roadmap](#roadmap--ideias-futuras).

## O processo de forja

O nome não é enfeite. O forje-ai trata um projeto como um ferreiro trata uma
lâmina: cada skill é uma etapa do ofício, e a ordem importa.

| Etapa da forja | Skill | O que acontece |
|---|---|---|
| 🔥 **Aquecer o metal bruto** | `forje-docs-bootstrap` | O repo cru vira material trabalhável: docs vivos, manifest, âncoras. Sem aquecer, todo golpe de martelo custa o dobro. |
| 🧪 **Provar no fogo** | `forje-grilling` | Antes de martelar, a ideia vai à brasa: o plano é interrogado até sobrar só o que aguenta o calor. |
| 🔨 **Martelar e moldar** | `forje-flow-feature` | A implementação em si — cada golpe guiado pelo contexto certo (`covers`/`summary`), nunca no escuro. |
| 🔍 **Inspecionar a lâmina** | `forje-code-review` | Olho de mestre no diff: read-only, evidência em mão, sem marteladas por impulso. |
| ⚔️ **Manter o fio** | `forje-docs-sync` | Lâmina sem manutenção perde o corte; doc sem sync perde a verdade. O fio se refaz a cada mudança. |
| 🧰 **A bancada** | `forje-registry` | O quadro de ferramentas na parede: o que existe e quando pegar cada uma. |
| ⚒️ **Forjar as ferramentas** | `forje-skill-authoring` | A forja que forja a si mesma: novas skills nascem aqui, nas mesmas convenções. |
| 👁️ **O aprendiz de olho** | hook `SessionStart` | Fica na porta da oficina: só fala quando a lâmina perdeu o fio (drift). Silêncio custa zero. |

Uma disciplina deliberada: **a metáfora vive aqui no README, não dentro das
skills**. Todo token dentro de um SKILL.md é pago quando a skill carrega; poesia
lá seria custo sem sinal. O ferreiro decora a oficina — nunca a lâmina.

## Números honestos

Inspirado no `HONEST-NUMBERS.md` do caveman: dizer o que é medido e o que é
hipótese.

- **Medido:** nada ainda. As afirmações de economia deste README derivam de
  aritmética de custos (o que entra no contexto e quantas vezes), não de
  benchmark próprio.
- **Hipótese central (testável):** docs vivos com `covers`/`summary`/âncoras
  previnem re-exploração — a maior fonte de gasto em trabalho agêntico. Um
  loop de grep/read evitado (~5–50k tokens) paga semanas do overhead fixo do
  plugin (~0,5–1k tokens/sessão em descriptions).
- **Como validar:** rodar 1–2 semanas com [codeburn](https://github.com/getagentseal/codeburn)
  observando arquivos relidos entre sessões, custo por sessão e taxa one-shot,
  antes e depois da adoção. Quando houver números, eles entram aqui —
  inclusive se forem ruins.

## Instalação

Pré-requisitos:

- [Claude Code](https://claude.com/claude-code) instalado;
- Python 3 com PyYAML — `python -m pip install -r requirements.txt` (ou
  `pip install pyyaml`). É usado pelos scripts de manutenção
  (`scripts/validate.py`, `scripts/gen_registry.py`) e pelo hook de
  `SessionStart`. **Sem PyYAML o plugin funciona, mas a sentinela de drift
  fica silenciosamente desativada** — o hook prefere calar a quebrar sua
  sessão.

### 1. Tenha o repo em algum lugar que o Claude Code alcance

Local (testando na sua própria máquina) ou um repo git remoto (GitHub, por
exemplo, se for instalar em outra máquina ou compartilhar com alguém):

```bash
git clone https://github.com/<seu-usuario>/forje-ai.git
```

### 2. Registre o marketplace

Dentro de uma sessão do Claude Code (em qualquer diretório):

```
/plugin marketplace add C:/caminho/onde/voce/clonou/forje-ai
```

— ou, se for a partir do GitHub:

```
/plugin marketplace add https://github.com/<seu-usuario>/forje-ai.git
```

### 3. Instale o plugin

```
/plugin install forje-ai@forje-ai
```

### 4. Habilite onde quiser usar

Por padrão o plugin fica disponível globalmente (escopo `user`) depois do
`install`. Para conferir ou desabilitar, `/plugin` abre o gerenciador
interativo. O que acontece por baixo dos panos é uma entrada em
`~/.claude/settings.json`:

```jsonc
{
  "enabledPlugins": {
    "forje-ai@forje-ai": true
  },
  "extraKnownMarketplaces": {
    "forje-ai": {
      "source": { "source": "git", "url": "https://github.com/<seu-usuario>/forje-ai.git" }
    }
  }
}
```

Editar esse arquivo direto funciona também, mas prefira os comandos `/plugin`
— eles cuidam do cache e do `installed_plugins.json` pra você.

## Como testar

Depois de instalado, abra o Claude Code em qualquer projeto pessoal (uma
pasta qualquer com código) e valide cada peça:

**1. As skills aparecem no picker.** Digite `/` e veja se
`forje-ai:forje-flow-feature` (e as demais) aparecem na lista — confirma que
o plugin foi instalado e o `SKILL.md` de cada uma tem YAML válido no
frontmatter (frontmatter quebrado faz a skill sumir da lista silenciosamente).

**2. Invocação por linguagem natural.** Sem digitar `/`, escreva um pedido
que bate com o gatilho de uma skill e veja se o Claude a invoca sozinho, por
exemplo:

```
revisa o código que eu acabei de escrever
```

Se ele mencionar que está usando `forje-code-review`, funcionou.

**3. Invocação explícita.** Se quiser forçar uma skill específica sem
depender do reconhecimento automático:

```
/forje-ai:forje-code-review
```

**4. Fluxo ponta a ponta.** O teste mais realista: pegue um projeto pessoal
pequeno (ou crie um de brinquedo) e rode o ciclo completo —
`forje-docs-bootstrap` para gerar os docs, depois peça uma feature pequena
(`forje-flow-feature` deve carregar os docs gerados em vez de vasculhar o
projeto do zero), depois `forje-code-review` no diff resultante.

## Como usar no dia a dia

Não existe comando a decorar — é conversa normal. Alguns exemplos de pedidos
e a skill que eles disparam:

| Você diz | Skill que entra em ação |
|---|---|
| "cria um endpoint que lista os pedidos do usuário" | `forje-flow-feature` |
| "revisa esse código antes de eu commitar" | `forje-code-review` |
| "gera os docs desse projeto, ele não tem nada documentado" | `forje-docs-bootstrap` |
| "os docs desse projeto parecem desatualizados" | `forje-docs-sync --report` |
| "acabei de mudar o fluxo de pagamento, atualiza os docs" | `forje-docs-sync --apply` |
| "me grilla sobre essa decisão de usar fila em vez de webhook" | `forje-grilling` |
| "quero criar uma skill nova pra mim" | `forje-skill-authoring` |

## As skills

### `forje-flow-feature` — implementar sem processo
Conduz uma feature, bug fix ou refactor do pedido até o código testado:
entende o pedido, carrega o `CLAUDE.md`/docs vivos do projeto (se existirem),
decide se vale a pena parar pra desenhar um plano antes de codar (mudança
trivial não precisa; mudança com decisão de design, sim — e se a decisão
abrir ramificações dependentes entre si, escala pra `forje-grilling` em vez
de uma confirmação única), implementa nas convenções que o próprio repo já
usa, e testa caminho feliz + um caso de erro. Sem card, sem aprovação
externa — só o suficiente pra não codar às cegas.

### `forje-code-review` — segundo par de olhos
Revisão do diff atual (ou de um branch específico), somente leitura.
Checklist enxuto: o código faz o que deveria e trata erro? Tem abstração
além do que a tarefa pedia? Tem segredo hardcoded, injeção, dependência
desnecessária? Cada achado vem com `arquivo:linha` e uma classificação
(bloqueante / importante / sugestão) — sem elogio vazio nem apontamento sem
prova.

### `forje-docs-sync` — mantém a documentação viva
Motor que compara os docs de contexto (`docs/*.md`, declarados num manifest
`.claude/context.yaml`) com o estado atual do código e aponta o que
divergiu. Roda em dois modos: `--report` (só lista o drift, não toca em
nada — usado antes de planejar a partir dos docs) e `--apply` (corrige os
docs, usado ao fim de uma implementação para registrar o que mudou). Essa
skill é o motivo pelo qual os docs não apodrecem depois da primeira semana.

### `forje-docs-bootstrap` — gera a documentação do zero
Para quando o projeto não tem nenhum doc de contexto ainda. Detecta o perfil
do projeto (backend .NET, Node, Python, frontend React/Vite) pela evidência
no próprio repo (`.csproj`, `package.json`, `pyproject.toml`...), confirma
com você o conjunto de docs a gerar, e produz um documento por vez — cada um
com uma leitura dedicada do código, nunca um "resumo geral" raso. Termina
criando o `.claude/context.yaml`, o manifest que o `forje-docs-sync` usa
depois.

### `forje-grilling` — me interroga antes de eu errar
Para decisões com várias ramificações dependentes ("se eu escolher A aqui,
isso muda o que faço em B e C lá na frente"), uma confirmação genérica
("faz sentido, pode seguir?") deixa passar a implicação escondida. Essa
skill faz uma entrevista: uma pergunta por vez, cada uma já com uma
recomendação e o porquê, nunca duas questões empacotadas juntas, só age
depois que não sobra ambiguidade nenhuma.

### `forje-skill-authoring` — como criar uma skill nova neste plugin
Meta-skill: convenções de nome, estrutura de arquivo, formato do
frontmatter e o checklist que eu sigo antes de considerar uma skill pronta —
sem aparato de compliance, só clareza e consistência.

## Por que "docs vivos" economiza token (e tempo)

Essa é a parte que mais vale a pena entender, porque não é óbvia à primeira
vista.

**O problema sem docs vivos.** Toda vez que você pede algo num projeto que o
Claude "não conhece" ainda, ele precisa reconstruir o entendimento do zero:
abrir a árvore de pastas, grepar por convenções, ler vários arquivos pra
inferir a arquitetura, entender as regras de negócio espalhadas pelo código.
Isso consome uma quantidade grande de tokens de contexto — e se repete **em
toda sessão nova**, porque o Claude não guarda memória de uma sessão pra
outra.

**O que o `forje-docs-bootstrap` faz.** Paga esse custo de exploração **uma
vez só**, de forma estruturada (um doc por vez, cada um com foco definido —
arquitetura, estrutura de pastas, convenções, regras de negócio), e grava o
resultado em markdown dentro do próprio repo. A partir daí, entender o
projeto não exige mais ler o código inteiro — basta ler 3 ou 4 arquivos de
doc, que são ordens de magnitude menores que a base de código completa.

**O que o `forje-docs-sync` faz com isso.** Em vez de reler os docs inteiros
contra o código inteiro a cada vez (o que ainda seria caro), cada doc guarda
seu próprio marcador (`synced_commit`, no manifest v2) e o sync só olha o
**diff** daquele doc desde a última conferência — `git log`/`git diff` num
punhado de arquivos, não uma auditoria completa. Doc de área fria não é
re-checado porque uma área quente mudou. Drift é a exceção, não a regra: a
maior parte das sessões não muda nada que os docs cobrem, então o `--report`
termina em segundos e sem gastar tokens lendo código que não mudou. As
afirmações dos docs carregam âncoras (`"pedidos expiram em 30 dias
(src/domain/Order.cs)"`), então verificar uma claim é abrir o arquivo
apontado, não caçar no código onde ela vive.

**O que o `.claude/context.yaml` faz com isso.** Cada doc declara quais
pastas (`covers`) ele descreve e um `summary` de uma linha (~20 tokens) com o
que ele afirma. Quando uma skill como `forje-flow-feature` precisa de
contexto, ela cruza a tarefa pedida com esse mapeamento e carrega **só os
docs relevantes** para aquela mudança — não o conjunto inteiro; empate no
`covers` se resolve lendo o `summary`, sem abrir doc nenhum. Uma tarefa que
mexe só no módulo de pagamento não carrega o doc de autenticação junto. Isso
mantém a janela de contexto enxuta mesmo em projetos com muitos documentos
acumulados.

Resumindo a cadeia: **bootstrap** troca "ler código toda sessão" por "ler
docs toda sessão" (muito mais barato) → **sync incremental** troca "reler
tudo" por "reler só o que mudou" (mais barato ainda) → **manifest com
`covers`** troca "carregar todos os docs" por "carregar só os docs
relevantes à tarefa" → **`summary` no manifest** troca "abrir o doc pra saber
se precisava dele" por "decidir lendo uma linha de metadado" (o resto do
orçamento de contexto sobra pro código em si, que é o que realmente importa
numa implementação).

> O formato completo do manifest (schema v2) está documentado em
> `skills/forje-docs-sync/SKILL.md`. Manifest antigo (v1, com
> `sync.last_synced_commit` global) ainda é entendido: o `--report` avisa e o
> `--apply` migra automaticamente.

## Estrutura do repo

```
forje-ai/
├── .claude-plugin/
│   ├── plugin.json         # manifesto do plugin (nome, versão, descrição)
│   └── marketplace.json    # manifesto do marketplace (como instalar)
├── .github/workflows/
│   └── validate.yml        # CI: valida frontmatters, versões e registry
├── scripts/
│   ├── validate.py         # validação local (mesma do CI)
│   └── gen_registry.py     # gera a tabela do forje-registry dos frontmatters
├── hooks/
│   ├── hooks.json          # registra o hook de SessionStart
│   └── session_start.py    # sentinela de drift: só fala se houver drift
├── skills/
│   ├── forje-registry/         # índice — leia primeiro pra saber o que existe
│   ├── forje-flow-feature/     # implementar sem processo
│   ├── forje-code-review/      # revisão pessoal
│   ├── forje-docs-sync/        # mantém docs vivos em dia
│   ├── forje-docs-bootstrap/   # gera docs vivos do zero
│   ├── forje-grilling/         # entrevista antes de decisão não-trivial
│   └── forje-skill-authoring/  # como criar uma skill nova aqui
├── README.md        # este arquivo, em português
└── README.en.md      # versão em inglês
```

## Como adicionar uma skill nova

1. Crie `skills/<nome>/SKILL.md` com frontmatter `name` (igual ao nome da
   pasta) + `description` (o que faz + quando invocar, em 1-2 frases — é o
   texto que decide se o Claude reconhece o gatilho).
2. Siga a estrutura e o checklist em `forje-skill-authoring` — corpo curto,
   passos numerados, regras duras só quando existir algo que nunca deve
   acontecer.
3. Liste a skill na tabela de `skills/forje-registry/SKILL.md`.
4. Se a mudança for algo que vale distribuir (nova skill, ajuste de
   comportamento), suba a versão em `.claude-plugin/plugin.json` **e**
   `.claude-plugin/marketplace.json` (mesmo número nos dois) — isso é o que
   permite quem já instalou notar que há uma atualização.

## Roadmap / ideias futuras

- `hooks/` com `SessionStart` — se algum dia eu quiser que o índice de
  skills seja sempre carregado, em vez de depender do reconhecimento por
  descrição.
- Skill de setup de projeto novo (`forje-flow-init`?) — scaffolding de
  linguagem/framework preferido, já com `.gitignore`, lint e teste
  configurados.

## Licença

MIT — veja [`LICENSE`](./LICENSE). Use, copie, modifique e redistribua à
vontade; mantenha o aviso de copyright.
