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
