# Tasks

## 1. Backend (Xano) — autenticação

- [x] 1.1 Corrigir `auth/login` (campos `Name`/`Password`, mensagem em português, log sem hash) e verificar com chamadas HTTP que o login devolve `authToken`
- [x] 1.2 Em `auth/signup`, checar e-mail e telefone duplicados com mensagem amigável e log sem hash, e verificar com chamadas HTTP que telefone repetido devolve 400 "Este telefone já está cadastrado."
- [x] 1.3 Corrigir `auth/me` (campo `Name`) e remover o hash dos logs de `reset/update_password` e `reset/magic-link-login`; verificar que o validador do XanoScript aceita os arquivos
- [x] 1.4 Exigir login em `message/send_welcome_email` e restringir ao próprio usuário; verificar com o validador

## 2. Backend (Xano) — controle de acesso

- [x] 2.1 Proteger o CRUD de `disponibilidade` (auth, dono = token, listagem própria, 403 para registros alheios) e verificar com chamadas HTTP usando dois alunos
- [x] 2.2 Proteger o CRUD de `usuario_disciplina` com as mesmas regras e verificar com chamadas HTTP usando dois alunos
- [x] 2.3 Proteger o CRUD de `match_interesse` (origem = token, sem interesse em si mesmo, só o alvo muda status, só a origem apaga) e verificar com chamadas HTTP
- [x] 2.4 Restringir a escrita de `curso` e `disciplina` a `admin` e verificar com chamadas HTTP que um `member` recebe 403 e que `GET /curso` continua público
- [x] 2.5 Criar a função `StudyMatch/excluir_usuario` (cascata em transação) e o endpoint `DELETE /auth/me`; verificar com chamadas HTTP que a conta apagada não loga mais (o `table_trigger` foi descartado porque o plano free não tem triggers)

## 3. Publicação

- [x] 3.1 Rodar `xano workspace push --dry-run`, revisar a prévia e publicar com `xano workspace push`; verificar com `xano workspace pull` em pasta temporária que o remoto ficou igual ao local

## 4. Frontend (Streamlit)

- [x] 4.1 Nenhuma alteração de frontend nesta change (o frontend começa na change `frontend-base-streamlit`); verificar que `git diff` não toca em arquivos Python
