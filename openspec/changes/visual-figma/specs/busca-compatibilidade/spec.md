# Spec Delta

## RENAMED Requirements

- FROM: `### Requirement: Página Buscar colegas`
- TO: `### Requirement: Colegas compatíveis no Início`

## MODIFIED Requirements

### Requirement: Colegas compatíveis no Início
A página "Início" SHALL mostrar a lista de `GET /compativeis` em cartões com o selo de compatibilidade, as disciplinas e os horários em comum e o sobre mim, com filtro por matéria e semestre e ordenação, e SHALL permitir demonstrar interesse com o botão "Dar match".

#### Scenario: Demonstrar interesse pela tela
- **WHEN** o aluno clica em "Dar match" em um colega
- **THEN** o interesse é enviado e o cartão passa a mostrar "Interesse enviado"

#### Scenario: Nenhum colega compatível
- **WHEN** a lista vem vazia
- **THEN** a página orienta o aluno a revisar as disciplinas e os horários em "Meu perfil"
