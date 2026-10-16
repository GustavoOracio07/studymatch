# Proposal

## Why

O backend já está protegido, mas não há interface: `app.py` só mostra uma mensagem de teste. O aluno precisa conseguir se cadastrar, entrar e sair pelo navegador. Essa é a base em que as próximas telas (perfil, busca e matches) serão montadas.

## What Changes

- Estrutura de páginas do Streamlit com `st.navigation`. Visitantes veem só "Entrar" e "Criar conta". Alunos logados veem "Início" e "Sair" (as demais páginas entram nas próximas changes).
- Cliente único da API do Xano (`studymatch/api.py`). A URL base vem da variável de ambiente `XANO_API_URL` ou de `.streamlit/secrets.toml`. O cliente envia o token, traduz os erros do Xano em mensagens legíveis e trata o limite de requisições do plano free.
- Tela de login (e-mail e senha) usando `POST /auth/login`.
- Tela de cadastro (nome, sobrenome, e-mail, senha, telefone, curso, semestre e sobre mim) usando `GET /curso` e `POST /auth/signup`. Após o cadastro, o aluno já entra logado.
- Logout: descarta o token da sessão e volta para a tela de login.
- Tela inicial do aluno logado, com saudação a partir de `GET /auth/me`.
- `.streamlit/secrets.toml.example` como modelo de configuração (o `secrets.toml` real continua fora do Git).

**Fora do escopo:**
- Edição de perfil, disciplinas e disponibilidade (change `perfil-aluno`).
- Busca de compatíveis e matches (changes seguintes).
- Recuperação de senha e "lembrar-me" entre sessões do navegador.
- Conversão do `requirements.txt` para UTF-8 e deploy (change de deploy).

## Capabilities

### New Capabilities
- `interface-web`: navegação do app Streamlit, acesso a páginas conforme login, telas de login, cadastro e logout, e exibição dos erros da API.

### Modified Capabilities
<!-- Nenhuma: as regras de autenticação do backend não mudam. -->

## Impact

- Novos arquivos: `studymatch/` (cliente da API e sessão), `paginas/` (telas), `.streamlit/secrets.toml.example`.
- `app.py` passa a ser o ponto de entrada com a navegação.
- Nenhuma mudança no Xano.
