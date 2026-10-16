# busca-compatibilidade Specification

## Purpose
Calcula quão compatíveis dois alunos são para estudar juntos e lista para o aluno os colegas compatíveis, sem expor dados de contato.

## Requirements

### Requirement: Cálculo da compatibilidade
O percentual de compatibilidade entre os alunos A e B SHALL ser `round(60 × D + 40 × H)`, de 0 a 100, onde:
- D = (disciplinas de dificuldade em comum) ÷ (menor quantidade de disciplinas entre A e B), ou 0 se algum dos dois não tiver disciplinas;
- H = (minutos de disponibilidade em comum no mesmo dia da semana) ÷ (menor total de minutos disponíveis entre A e B), ou 0 se algum dos dois não tiver horários.

O cálculo SHALL ser simétrico (A com B dá o mesmo resultado que B com A).

#### Scenario: Mesmas disciplinas e mesmos horários
- **WHEN** A e B têm exatamente as mesmas disciplinas e os mesmos horários
- **THEN** o percentual é 100

#### Scenario: Disciplinas em comum sem horário em comum
- **WHEN** A tem as disciplinas {1, 2}, B tem {1} e eles não têm horários em comum
- **THEN** o percentual é 60

#### Scenario: Metade do horário em comum
- **WHEN** A e B têm a mesma disciplina, A está livre segunda das 09:00 às 11:00 e B segunda das 10:00 às 14:00
- **THEN** H = 60 ÷ 120 = 0,5 e o percentual é 80

### Requirement: Lista de colegas compatíveis
`GET /compativeis` SHALL devolver, para o aluno do token, os outros alunos com pelo menos uma disciplina de dificuldade em comum, em ordem decrescente de percentual. Cada item SHALL ter id, nome, sobrenome, semestre, sobre mim, percentual, ids das disciplinas em comum, horários em comum e a situação do interesse entre os dois (`nenhum`, `enviado`, `recebido`, `match` ou `recusado`). A resposta SHALL NOT conter telefone nem e-mail.

#### Scenario: Colega com disciplina em comum
- **WHEN** o aluno A chama `GET /compativeis` e o aluno B tem uma disciplina de dificuldade em comum com A
- **THEN** B aparece na lista com o percentual calculado e `situacao = "nenhum"`

#### Scenario: Colega sem disciplina em comum
- **WHEN** o aluno C não tem nenhuma disciplina de dificuldade em comum com A
- **THEN** C não aparece na lista de A

#### Scenario: Sem dados de contato
- **WHEN** A recebe a lista
- **THEN** nenhum item contém `Telefone` nem `email`

#### Scenario: Sem token
- **WHEN** um cliente chama `GET /compativeis` sem token
- **THEN** o sistema responde 401

### Requirement: Colegas compatíveis no Início
A página "Início" SHALL mostrar a lista de `GET /compativeis` em cartões com o selo de compatibilidade, as disciplinas e os horários em comum e o sobre mim, com filtro por matéria e semestre e ordenação, e SHALL permitir demonstrar interesse com o botão "Dar match".

#### Scenario: Demonstrar interesse pela tela
- **WHEN** o aluno clica em "Dar match" em um colega
- **THEN** o interesse é enviado e o cartão passa a mostrar "Interesse enviado"

#### Scenario: Nenhum colega compatível
- **WHEN** a lista vem vazia
- **THEN** a página orienta o aluno a revisar as disciplinas e os horários em "Meu perfil"
