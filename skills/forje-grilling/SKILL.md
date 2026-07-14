---
name: forje-grilling
description: Interroga o Lucas sobre um plano, decisão ou ideia até alcançar entendimento compartilhado — uma pergunta por vez, sempre com uma recomendação, sem agir até confirmação explícita. Use quando ele pedir para "stress-testar" uma decisão, disser "me grilla sobre X", "quero validar essa ideia antes de codar", ou quando outra skill deste plugin encontrar uma decisão não-trivial no passo de clarificação.
---

# Grilling

Confirmação única ("faz sentido, pode seguir?") não pega decisão errada quando o
plano tem ramificações dependentes entre si — a resposta a uma pergunta genérica
esconde a implicação específica lá na frente. Esta skill substitui isso por uma
entrevista: uma pergunta por vez, cada uma com recomendação, descendo a árvore de
decisão até não sobrar ambiguidade.

## Fluxo

1. **Mapear a árvore de decisão** — antes de perguntar qualquer coisa, liste
   mentalmente quais escolhas o plano/ideia exige e quais dependem de outras.
2. **Resolver sozinho o que for descobrível** — o que estiver no código, configs,
   docs do repo ou histórico do git, investigue antes de perguntar. Só leve ao
   Lucas o que for de fato uma escolha dele.
3. **Perguntar uma de cada vez** — apresente a pergunta junto da sua recomendação e
   o porquê. Aguarde a resposta antes de formular a próxima. Nunca empacote duas
   perguntas na mesma mensagem.
4. **Descer por dependência, não por lista fixa** — a resposta de uma pergunta pode
   abrir, fechar ou reformular ramos seguintes; siga a ramificação que a resposta
   realmente abriu.
5. **Fechar com o entendimento compartilhado** — quando não houver mais ambiguidade,
   resuma as decisões tomadas em poucas linhas e peça confirmação explícita. Só
   depois disso é hora de agir — implementar, planejar, escrever.

## Regras duras

- Nunca faça duas perguntas na mesma mensagem.
- Nunca pergunte o que já é descobrível no ambiente (arquivo, config, git log) —
  investigue antes de levar ao Lucas.
- Nunca comece a agir sobre o plano/decisão antes da confirmação explícita.
- Sempre traga uma recomendação junto de cada pergunta.
