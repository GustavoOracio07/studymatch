# Spec Delta

## ADDED Requirements

### Requirement: Foto nos meus matches
Cada item de `GET /meus_matches` SHALL incluir `foto_url` do colega (`null` sem foto), em qualquer status, e o card na página Meus matches SHALL mostrar a foto ou o avatar com as iniciais.

#### Scenario: Pedido pendente com foto
- **WHEN** B, que tem foto, demonstra interesse em A e A chama `GET /meus_matches`
- **THEN** o item do pedido traz `foto_url` de B e continua sem o telefone de B

#### Scenario: Match confirmado com foto
- **WHEN** A e B têm match confirmado e B tem foto
- **THEN** o card de B em Meus matches mostra a foto e o telefone de B
