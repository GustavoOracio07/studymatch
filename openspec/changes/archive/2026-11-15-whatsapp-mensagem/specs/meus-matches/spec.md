# Spec Delta

## ADDED Requirements

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
