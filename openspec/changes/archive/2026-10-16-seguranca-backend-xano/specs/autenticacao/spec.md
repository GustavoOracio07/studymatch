# Spec Delta

## Purpose

Define como o aluno se cadastra e entra no StudyMatch, quais mensagens recebe em caso de erro e como os eventos de autenticação são registrados sem expor dados sensíveis.

## ADDED Requirements

### Requirement: Login com e-mail e senha
O sistema SHALL autenticar o aluno por e-mail e senha e devolver um token de acesso e o `user_id`.

#### Scenario: Credenciais corretas
- **WHEN** o aluno envia `POST /auth/login` com e-mail e senha corretos
- **THEN** o sistema responde 200 com `authToken` e `user_id`

#### Scenario: Senha incorreta
- **WHEN** o aluno envia `POST /auth/login` com senha errada
- **THEN** o sistema responde 403 com a mensagem "E-mail ou senha inválidos."

#### Scenario: E-mail inexistente
- **WHEN** o aluno envia `POST /auth/login` com um e-mail não cadastrado
- **THEN** o sistema responde 403 com a mesma mensagem "E-mail ou senha inválidos."

### Requirement: Cadastro com dados únicos
O sistema SHALL recusar o cadastro quando o e-mail ou o telefone já pertencerem a outro aluno, com mensagem amigável em português.

#### Scenario: Cadastro válido
- **WHEN** o aluno envia `POST /auth/signup` com e-mail e telefone ainda não usados
- **THEN** o sistema cria o aluno com papel `member` e responde 200 com `authToken` e `user_id`

#### Scenario: Telefone duplicado
- **WHEN** o aluno envia `POST /auth/signup` com um telefone já cadastrado
- **THEN** o sistema responde 400 com a mensagem "Este telefone já está cadastrado." e nenhum usuário é criado

#### Scenario: E-mail duplicado
- **WHEN** o aluno envia `POST /auth/signup` com um e-mail já cadastrado
- **THEN** o sistema responde 400 com a mensagem "Este e-mail já está cadastrado." e nenhum usuário é criado

### Requirement: Registro de eventos sem dados sensíveis
O sistema SHALL registrar eventos de autenticação no `event_log` sem incluir a senha nem o hash da senha.

#### Scenario: Log do login
- **WHEN** um aluno faz login com sucesso
- **THEN** o registro criado no `event_log` com `action = "login"` não contém o campo `Password` nem qualquer hash de senha

#### Scenario: Log do cadastro
- **WHEN** um aluno se cadastra com sucesso
- **THEN** o registro criado no `event_log` com `action = "signup"` não contém o campo `Password` nem qualquer hash de senha
