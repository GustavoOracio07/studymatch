# Spec Delta

## ADDED Requirements

### Requirement: Foto dos colegas compatíveis
Cada item de `GET /compativeis` SHALL incluir `foto_url` do colega (`null` sem foto), sem expor os metadados do arquivo, e o card do colega no Início SHALL mostrar a foto ou o avatar com as iniciais.

#### Scenario: Colega com foto
- **WHEN** o aluno A é compatível com B, que tem foto, e A chama `GET /compativeis`
- **THEN** o item de B traz `foto_url` preenchido e não traz o objeto `Foto` nem `path`

#### Scenario: Colega sem foto
- **WHEN** o aluno A é compatível com C, que não tem foto
- **THEN** o item de C traz `foto_url` nulo e o card de C no Início mostra as iniciais de C
