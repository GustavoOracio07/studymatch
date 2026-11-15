# meus-matches Specification

## Purpose
Mostra ao aluno os interesses que recebeu, os que enviou e os matches confirmados, permite responder aos pedidos e libera o telefone do colega somente depois do match.

## Requirements

### Requirement: Listar meus matches
`GET /meus_matches` SHALL devolver, para o aluno do token, as listas `recebidos` (pendentes em que ele é o alvo), `enviados` (pendentes ou recusados em que ele é a origem) e `confirmados` (status `match`, como origem ou alvo). Cada item SHALL ter `interesse_id`, `status`, `percentual` e os dados do colega: `usuario_id`, `nome`, `sobrenome`, `semestre` e `sobre_mim`. Registros cujo colega não existe mais SHALL ser ignorados.

#### Scenario: Pedido recebido
- **WHEN** B enviou interesse para A e A chama `GET /meus_matches`
- **THEN** o pedido aparece em `recebidos` de A com os dados de B

#### Scenario: Pedido enviado e recusado
- **WHEN** A enviou interesse para C e C recusou
- **THEN** o pedido aparece em `enviados` de A com `status = "recusado"`

#### Scenario: Sem token
- **WHEN** um cliente chama `GET /meus_matches` sem token
- **THEN** o sistema responde 401

### Requirement: Telefone só após o match confirmado
O telefone do colega SHALL aparecer apenas nos itens de `confirmados`, e SHALL NOT aparecer em `recebidos` nem em `enviados`.

#### Scenario: Pedido pendente
- **WHEN** A tem um pedido pendente com B
- **THEN** o item de B em `recebidos` ou `enviados` não contém telefone

#### Scenario: Match confirmado
- **WHEN** A aceita o interesse de B
- **THEN** o item de B em `confirmados` de A contém o `telefone` de B, e o item de A em `confirmados` de B contém o `telefone` de A

### Requirement: Página Meus matches
O app SHALL ter a página "Meus matches", com as abas Recebidos, Enviados e Confirmados. Em Recebidos há os botões Aceitar e Recusar; em Enviados pendentes, o botão Cancelar interesse; em Confirmados, o telefone do colega.

#### Scenario: Aceitar pela tela
- **WHEN** o aluno clica em "Aceitar" em um pedido recebido
- **THEN** o pedido sai de Recebidos e aparece em Confirmados com o telefone do colega

#### Scenario: Recusar pela tela
- **WHEN** o aluno clica em "Recusar" em um pedido recebido
- **THEN** o pedido sai de Recebidos e o telefone do colega não é exibido

#### Scenario: Cancelar interesse enviado
- **WHEN** o aluno clica em "Cancelar interesse" em um pedido enviado pendente
- **THEN** o pedido sai de Enviados

### Requirement: Foto nos meus matches
Cada item de `GET /meus_matches` SHALL incluir `foto_url` do colega (`null` sem foto), em qualquer status, e o card na página Meus matches SHALL mostrar a foto ou o avatar com as iniciais.

#### Scenario: Pedido pendente com foto
- **WHEN** B, que tem foto, demonstra interesse em A e A chama `GET /meus_matches`
- **THEN** o item do pedido traz `foto_url` de B e continua sem o telefone de B

#### Scenario: Match confirmado com foto
- **WHEN** A e B têm match confirmado e B tem foto
- **THEN** o card de B em Meus matches mostra a foto e o telefone de B

### Requirement: Disciplinas em comum nos matches confirmados
Cada item de `confirmados` em `GET /meus_matches` SHALL incluir `disciplinas_comuns`, a lista dos ids das disciplinas de dificuldade que o aluno do token e o colega têm em comum no momento da consulta. Os itens de `recebidos` e `enviados` SHALL NOT incluir esse campo.

#### Scenario: Match com disciplinas em comum
- **WHEN** A e B têm a disciplina 1 em comum e um match confirmado, e A chama `GET /meus_matches`
- **THEN** o item de B em `confirmados` traz `disciplinas_comuns = [1]`

#### Scenario: Match sem disciplina em comum
- **WHEN** A e B têm um match confirmado, mas não têm mais nenhuma disciplina em comum
- **THEN** o item de B em `confirmados` traz `disciplinas_comuns = []`

#### Scenario: Pedido pendente
- **WHEN** A tem um pedido pendente com B
- **THEN** o item de B em `recebidos` ou `enviados` não contém `disciplinas_comuns`

### Requirement: Chamar no WhatsApp
Cada match confirmado na página Meus matches SHALL ter o botão "Chamar no WhatsApp", que abre `https://wa.me/<número>` com uma mensagem pronta. Telefones com 10 ou 11 dígitos SHALL ganhar o DDI 55. A mensagem SHALL cumprimentar o colega pelo nome e, quando houver disciplinas em comum, SHALL citar os nomes delas. Sem um telefone com pelo menos 12 dígitos (já com o DDI), o botão SHALL NOT aparecer.

#### Scenario: Mensagem com disciplinas em comum
- **WHEN** A tem match confirmado com Ana, telefone `11973358648`, e as duas têm "Cálculo I" e "Banco de Dados" em comum
- **THEN** o botão abre `https://wa.me/5511973358648` com o texto "Oi, Ana! Deu match no StudyMatch: temos dificuldade em Cálculo I e Banco de Dados. Bora marcar um horário para estudar juntos?"

#### Scenario: Mensagem sem disciplina em comum
- **WHEN** o match confirmado não tem nenhuma disciplina em comum
- **THEN** o botão abre o WhatsApp com o texto "Oi, Ana! Deu match no StudyMatch. Bora marcar um horário para estudar juntos?"

#### Scenario: Telefone inválido
- **WHEN** o telefone do colega tem menos de 10 dígitos
- **THEN** o cartão do match mostra o telefone, mas não mostra o botão "Chamar no WhatsApp"
