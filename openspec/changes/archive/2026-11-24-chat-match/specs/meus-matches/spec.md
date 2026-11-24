# Spec Delta

## ADDED Requirements

### Requirement: Abrir a conversa pelo match
Cada match confirmado na página Meus matches SHALL ter o botão "Conversar", que abre a conversa com aquele colega. Pedidos recebidos e enviados SHALL NOT ter esse botão.

#### Scenario: Match confirmado
- **WHEN** o aluno clica em "Conversar" em um match confirmado
- **THEN** a página da conversa abre com o nome do colega

#### Scenario: Pedido não confirmado
- **WHEN** o aluno vê um pedido em Recebidos ou Enviados
- **THEN** o cartão não tem o botão "Conversar"
