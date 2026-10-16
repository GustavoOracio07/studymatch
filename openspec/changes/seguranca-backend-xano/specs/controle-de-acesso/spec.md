# Spec Delta

## Purpose

Garante no backend que cada aluno só lê e altera os próprios dados, que cursos e disciplinas não são editados pelo app e que os dados dependentes são removidos quando um usuário é apagado.

## ADDED Requirements

### Requirement: Endpoints protegidos exigem login
Os endpoints que leem dados pessoais ou alteram dados SHALL exigir um token válido. Leitura de `curso` e `disciplina` continua pública.

#### Scenario: Requisição sem token
- **WHEN** um cliente chama `POST /disponibilidade` sem o cabeçalho `Authorization`
- **THEN** o sistema responde 401 e nada é gravado

#### Scenario: Leitura pública de cursos
- **WHEN** um cliente chama `GET /curso` sem token
- **THEN** o sistema responde 200 com a lista de cursos

### Requirement: Dono do registro é o usuário do token
Ao criar `disponibilidade`, `usuario_disciplina` ou `match_interesse`, o sistema SHALL gravar o usuário do token como dono (`usuario_id`), ignorando qualquer `usuario_id` enviado pelo cliente.

#### Scenario: Tentativa de criar em nome de outro aluno
- **WHEN** o aluno 2 chama `POST /disponibilidade` enviando `usuario_id = 1`
- **THEN** o registro é criado com `usuario_id = 2`

### Requirement: Listagens restritas ao próprio aluno
As listagens de `disponibilidade` e `usuario_disciplina` SHALL devolver apenas os registros do usuário do token. A listagem de `match_interesse` SHALL devolver apenas os registros em que ele é origem ou alvo.

#### Scenario: Listar disponibilidades
- **WHEN** o aluno 2 chama `GET /disponibilidade`
- **THEN** a resposta contém apenas registros com `usuario_id = 2`

#### Scenario: Ler registro de outro aluno
- **WHEN** o aluno 2 chama `GET /disponibilidade/{id}` de um registro do aluno 1
- **THEN** o sistema responde 403

### Requirement: Edição e exclusão apenas pelo dono
O sistema SHALL permitir editar ou apagar `disponibilidade` e `usuario_disciplina` somente ao dono do registro, sem permitir trocar o dono.

#### Scenario: Apagar registro próprio
- **WHEN** o aluno 2 chama `DELETE /disponibilidade/{id}` de um registro dele
- **THEN** o sistema responde 200 e o registro é apagado

#### Scenario: Apagar registro de outro aluno
- **WHEN** o aluno 2 chama `DELETE /disponibilidade/{id}` de um registro do aluno 1
- **THEN** o sistema responde 403 e o registro continua existindo

### Requirement: Regras de acesso do interesse de match
No `match_interesse`, o sistema SHALL permitir que apenas o aluno alvo altere o status, apenas de `pendente` para `match` ou `recusado`, e que apenas o aluno de origem apague o interesse. Um aluno SHALL NOT criar interesse em si mesmo.

#### Scenario: Alvo aceita o interesse
- **WHEN** o aluno alvo chama `PATCH /match_interesse/{id}` com `status = "match"` em um interesse pendente
- **THEN** o status passa para `match`

#### Scenario: Origem tenta aceitar o próprio interesse
- **WHEN** o aluno de origem chama `PATCH /match_interesse/{id}` com `status = "match"`
- **THEN** o sistema responde 403 e o status não muda

#### Scenario: Interesse em si mesmo
- **WHEN** o aluno chama `POST /match_interesse` com `usuario_alvo_id` igual ao próprio id
- **THEN** o sistema responde 400 e nada é gravado

### Requirement: Cursos e disciplinas não são editados pelo app
Os endpoints de criação, edição e exclusão de `curso` e `disciplina` SHALL exigir usuário com papel `admin`.

#### Scenario: Aluno tenta criar curso
- **WHEN** um aluno com papel `member` chama `POST /curso`
- **THEN** o sistema responde 403 e nada é gravado

### Requirement: Exclusão em cascata do usuário
Quando um usuário é apagado, o sistema SHALL apagar as disponibilidades e as disciplinas de dificuldade dele.

#### Scenario: Usuário apagado
- **WHEN** um usuário com disponibilidades e disciplinas de dificuldade é apagado
- **THEN** não resta nenhum registro de `disponibilidade` nem de `usuario_disciplina` com o `usuario_id` dele
