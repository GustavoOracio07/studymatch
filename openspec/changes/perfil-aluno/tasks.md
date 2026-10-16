# Tasks

## 1. Backend (Xano)

- [ ] 1.1 Ampliar o `GET /auth/me` e criar o `PATCH /auth/me` (semestre, telefone único, curso existente, troca de curso limpa disciplinas, resposta sem senha); verificar com `tests/api/teste_perfil.py`
- [ ] 1.2 Criar a função `validar_disciplina_do_curso`, usá-la em POST/PATCH de `usuario_disciplina` (com checagem de repetida) e criar o `PUT /minhas_disciplinas`; verificar com `tests/api/teste_perfil.py`
- [ ] 1.3 Criar a função `validar_disponibilidade` e usá-la em POST/PATCH de `disponibilidade`; verificar formato, meia-noite, sobreposição e faixas encostadas com `tests/api/teste_perfil.py`
- [ ] 1.4 Validar os `.xs`, rodar `xano workspace push --dry-run`, publicar e alinhar o local com `xano workspace pull`; verificar que o dry-run final diz "No changes to push"
- [ ] 1.5 Rodar de novo `tests/api/teste_seguranca.py` e verificar que as regras de acesso continuam passando

## 2. Frontend (Streamlit)

- [ ] 2.1 Adicionar ao cliente os métodos de perfil, disciplinas e disponibilidade; verificar com `tests/frontend/teste_api_cliente.py`
- [ ] 2.2 Criar a página "Meu perfil" (abas Dados, Disciplinas e Disponibilidade) e incluí-la na navegação; verificar com `tests/frontend/teste_telas_perfil.py` (salvar dados, escolher disciplinas do curso, faixa sobreposta mostra o erro)
