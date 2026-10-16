# Proposal

## Why

O aluno já consegue demonstrar interesse, mas não tem onde ver quem demonstrou interesse nele, responder esses pedidos ou acompanhar os que enviou. Depois do match, falta o passo final do produto: mostrar o telefone para os dois combinarem o estudo. Pela regra do domínio, isso só pode acontecer após o match confirmado.

## What Changes

- Novo `GET /meus_matches`: devolve, para o aluno do token, três listas:
  - **recebidos**: interesses pendentes em que ele é o alvo;
  - **enviados**: interesses que ele enviou, pendentes ou recusados;
  - **confirmados**: matches dos quais ele participa.

  Cada item traz os dados públicos do colega (nome, sobrenome, semestre, sobre mim) e o percentual. **O telefone só aparece nos confirmados.** Registros de colegas que apagaram a conta são ignorados.
- A resposta aos pedidos usa o `PATCH /match_interesse/{id}`, que já existe (só o alvo, só pendente). Cancelar um interesse enviado e ainda pendente usa o `DELETE /match_interesse/{id}`, que também já existe (só a origem).
- **BREAKING (pequeno)**: o `DELETE /match_interesse/{id}` passa a aceitar só interesses pendentes. Um match confirmado não pode ser desfeito pela origem sozinha.
- Nova página "Meus matches" no Streamlit, com as abas Recebidos, Enviados e Confirmados, e os botões Aceitar, Recusar e Cancelar interesse.

**Fora do escopo:**
- Desfazer um match confirmado.
- Chat, notificações por e-mail/push e grupos (fora do escopo do MVP).
- Exibir o e-mail do colega (a decisão do domínio fala só do telefone).

## Capabilities

### New Capabilities
- `meus-matches`: listagem dos interesses recebidos, enviados e confirmados, resposta aos pedidos e exibição do telefone só após o match.

### Modified Capabilities
- `controle-de-acesso`: a exclusão de interesse pela origem passa a valer só para interesse pendente.

## Impact

- Xano: novo endpoint `meus_matches` (GET) e ajuste em `match_interesse/{id}` (DELETE).
- Streamlit: nova página `paginas/matches.py` e novos métodos no cliente.
