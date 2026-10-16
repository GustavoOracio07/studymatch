# Tasks

## 1. Backend (Xano)

- [ ] 1.1 Nenhuma alteração no Xano; verificar com `xano workspace push --dry-run` que não há mudanças pendentes

## 2. Frontend (Streamlit) — infraestrutura

- [ ] 2.1 Criar `studymatch/api.py` (cliente `XanoAPI`, `ErroAPI`, tratamento de 401/429/rede) e verificar com `tests/frontend/teste_api_cliente.py` (respostas simuladas)
- [ ] 2.2 Criar `studymatch/sessao.py` (entrar, sair, aluno atual) e `.streamlit/secrets.toml.example`; verificar que `secrets.toml` continua ignorado com `git check-ignore`
- [ ] 2.3 Reescrever `app.py` com `st.navigation` (páginas de visitante e de aluno) e verificar com `AppTest` que o visitante vê a página "Entrar"

## 3. Frontend (Streamlit) — telas

- [ ] 3.1 Criar a tela "Entrar" e verificar com `AppTest` contra a API: login correto leva ao "Início" e senha errada mostra "E-mail ou senha inválidos."
- [ ] 3.2 Criar a tela "Criar conta" e verificar com `AppTest` que o cadastro entra logado e que o telefone repetido mostra a mensagem da API
- [ ] 3.3 Criar as telas "Início" e "Sair" e verificar com `AppTest` que sair limpa o token e volta para "Entrar"
- [ ] 3.4 Subir o app com `streamlit run app.py` e verificar que `/_stcore/health` responde `ok`
