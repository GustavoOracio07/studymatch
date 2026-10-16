# Spec Delta

## Purpose

Define a interface web em Streamlit do StudyMatch: como o aluno navega, entra, cria a conta e sai, e como os erros vindos da API do Xano aparecem na tela.

## ADDED Requirements

### Requirement: Navegação conforme o login
O app SHALL mostrar apenas as páginas "Entrar" e "Criar conta" para visitantes, e as páginas do aluno (incluindo "Sair") para quem está logado.

#### Scenario: Visitante abre o app
- **WHEN** um visitante sem sessão abre o app
- **THEN** a página "Entrar" é exibida e as páginas do aluno não aparecem no menu

#### Scenario: Aluno logado abre o app
- **WHEN** um aluno com token na sessão abre o app
- **THEN** a página "Início" é exibida com a saudação "Olá, <nome>!" e o menu mostra "Sair"

### Requirement: Login pela interface
O app SHALL permitir entrar com e-mail e senha e guardar o token na sessão do navegador.

#### Scenario: Login bem-sucedido
- **WHEN** o aluno informa e-mail e senha corretos e clica em "Entrar"
- **THEN** o token é guardado na sessão e o aluno é levado à página "Início"

#### Scenario: Login com senha errada
- **WHEN** o aluno informa uma senha errada
- **THEN** o app mostra a mensagem de erro devolvida pela API ("E-mail ou senha inválidos.") e continua na página "Entrar"

#### Scenario: Campos vazios
- **WHEN** o aluno clica em "Entrar" sem preencher e-mail ou senha
- **THEN** o app pede para preencher os campos e não chama a API

### Requirement: Cadastro pela interface
O app SHALL permitir criar a conta escolhendo o curso em uma lista vinda da API e SHALL entrar automaticamente após o cadastro.

#### Scenario: Cadastro bem-sucedido
- **WHEN** o visitante preenche todos os campos obrigatórios e clica em "Criar conta"
- **THEN** a conta é criada, o token é guardado na sessão e o aluno é levado à página "Início"

#### Scenario: Telefone já cadastrado
- **WHEN** o visitante usa um telefone que já pertence a outro aluno
- **THEN** o app mostra "Este telefone já está cadastrado." e continua na página "Criar conta"

### Requirement: Logout
O app SHALL permitir sair, descartando o token da sessão.

#### Scenario: Sair
- **WHEN** o aluno logado abre a página "Sair"
- **THEN** o token é removido da sessão e o app volta para a página "Entrar"

### Requirement: Sessão expirada ou API indisponível
O app SHALL tratar a sessão expirada e as falhas da API sem quebrar a tela.

#### Scenario: Token expirado
- **WHEN** a API responde 401 a uma chamada feita com o token da sessão
- **THEN** o app remove o token e pede para entrar de novo

#### Scenario: Limite de requisições
- **WHEN** a API responde 429
- **THEN** o app mostra "Muitas requisições em pouco tempo. Aguarde alguns segundos e tente de novo."
