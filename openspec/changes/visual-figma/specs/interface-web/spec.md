# Spec Delta

## MODIFIED Requirements

### Requirement: Navegação conforme o login
O app SHALL mostrar apenas as páginas "Entrar" e "Criar conta" para visitantes, sem menu lateral, e para quem está logado o menu lateral SHALL ter "Início", "Meus matches", "Meu perfil" e "Sair".

#### Scenario: Visitante abre o app
- **WHEN** um visitante sem sessão abre o app
- **THEN** a página "Entrar" é exibida com o painel "Bem-vindo ao StudyMatch" e as páginas do aluno não aparecem

#### Scenario: Aluno logado abre o app
- **WHEN** um aluno com token na sessão abre o app
- **THEN** a página "Início" é exibida com a saudação "Olá, <nome>!" e o menu mostra "Início", "Meus matches", "Meu perfil" e "Sair"

### Requirement: Cadastro pela interface
O app SHALL permitir criar a conta em 3 etapas — (1) nome e sobrenome, (2) senha, confirmação da senha e e-mail, (3) curso, semestre, telefone e sobre mim — escolhendo o curso em uma lista vinda da API, e SHALL entrar automaticamente após o cadastro. A API SHALL ser chamada só na última etapa.

#### Scenario: Cadastro bem-sucedido
- **WHEN** o visitante preenche as 3 etapas e clica em "Criar conta"
- **THEN** a conta é criada, o token é guardado na sessão e o aluno é levado à página "Início"

#### Scenario: Senhas diferentes
- **WHEN** a senha e a confirmação da etapa 2 são diferentes
- **THEN** o app mostra "As senhas não conferem." e continua na etapa 2

#### Scenario: Voltar uma etapa
- **WHEN** o visitante clica em "Voltar"
- **THEN** a etapa anterior é exibida com os dados já digitados

#### Scenario: Telefone já cadastrado
- **WHEN** o visitante usa um telefone que já pertence a outro aluno
- **THEN** o app mostra "Este telefone já está cadastrado." e continua na etapa 3
