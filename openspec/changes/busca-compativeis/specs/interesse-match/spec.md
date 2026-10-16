# Spec Delta

## Purpose

Define como um aluno demonstra interesse em estudar com outro, com o percentual calculado pelo backend e a regra de que o interesse cruzado vira match.

## ADDED Requirements

### Requirement: Percentual calculado pelo backend
Ao criar um interesse, o sistema SHALL calcular e gravar o percentual de compatibilidade, ignorando qualquer percentual enviado pelo cliente.

#### Scenario: Cliente envia percentual falso
- **WHEN** o aluno A chama `POST /match_interesse` para B enviando `percentual_compatibilidade = 100`
- **THEN** o registro é gravado com o percentual calculado entre A e B, com status `pendente`

### Requirement: Interesse cruzado vira match
Se B já tem um interesse pendente para A e A demonstra interesse em B, o sistema SHALL mudar o registro existente para `match` e SHALL NOT criar um novo registro.

#### Scenario: Interesse cruzado
- **WHEN** B já enviou interesse para A (pendente) e A chama `POST /match_interesse` para B
- **THEN** a resposta é o registro de B para A com `status = "match"`, e continua havendo só um registro entre os dois

### Requirement: Interesse repetido ou inválido
O sistema SHALL recusar interesse em si mesmo, em aluno inexistente, repetido ou entre alunos que já têm match.

#### Scenario: Interesse repetido
- **WHEN** A já enviou interesse para B e envia de novo
- **THEN** o sistema responde 400 com "Você já demonstrou interesse neste colega."

#### Scenario: Já existe match
- **WHEN** A e B já têm um match e A envia interesse para B
- **THEN** o sistema responde 400 com "Vocês já têm um match."

#### Scenario: Aluno inexistente
- **WHEN** A envia interesse para um id que não existe
- **THEN** o sistema responde 404 com "Aluno não encontrado."
