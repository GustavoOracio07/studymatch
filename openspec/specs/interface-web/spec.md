# interface-web Specification

## Purpose
Define a interface web em Streamlit do StudyMatch: como o aluno navega, entra, cria a conta e sai, e como os erros vindos da API do Xano aparecem na tela.

## Requirements

### Requirement: Navegação conforme o login
O app SHALL mostrar apenas as páginas "Entrar" e "Criar conta" para visitantes, sem menu lateral, e para quem está logado o menu lateral SHALL ter "Início", "Meus matches", "Meu perfil" e "Sair".

#### Scenario: Visitante abre o app
- **WHEN** um visitante sem sessão abre o app
- **THEN** a página "Entrar" é exibida com o painel "Bem-vindo ao StudyMatch" e as páginas do aluno não aparecem

#### Scenario: Aluno logado abre o app
- **WHEN** um aluno com token na sessão abre o app
- **THEN** a página "Início" é exibida com a saudação "Olá, <nome>!" e o menu mostra "Início", "Meus matches", "Meu perfil" e "Sair"

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

### Requirement: Modo claro e modo escuro
O app SHALL ter um botão para alternar entre modo claro e modo escuro — no menu lateral para o aluno logado e no canto da tela em "Entrar" e "Criar conta". A escolha SHALL valer em todas as páginas da sessão, inclusive depois de sair da conta.

#### Scenario: Ativar o modo escuro
- **WHEN** o aluno clica em "Modo escuro"
- **THEN** a interface passa a usar fundo escuro com destaques em roxo e o botão passa a se chamar "Modo claro"

#### Scenario: Trocar de página
- **WHEN** o modo escuro está ativo e o aluno abre outra página do menu
- **THEN** a nova página também aparece no modo escuro

#### Scenario: Sair da conta
- **WHEN** o modo escuro está ativo e o aluno clica em "Sair"
- **THEN** a tela "Entrar" aparece no modo escuro
