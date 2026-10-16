# Tasks

## 1. Backend (Xano)

- [x] 1.1 Criar a função `StudyMatch/calcular_compatibilidade` e verificar os cenários do spec (100, 60 e 80) com `tests/api/teste_busca.py`
- [x] 1.2 Criar `GET /compativeis` (só colegas com disciplina em comum, ordenado, com situação do interesse, sem telefone/e-mail) e verificar com `tests/api/teste_busca.py`
- [x] 1.3 Alterar `POST /match_interesse` (percentual do backend, interesse cruzado vira match, repetido/match/inexistente com mensagem) e verificar com `tests/api/teste_busca.py`
- [x] 1.4 Publicar com dry-run + push, alinhar o local com pull e verificar que `tests/api/teste_seguranca.py` continua passando

## 2. Frontend (Streamlit)

- [x] 2.1 Adicionar `compativeis()` e `demonstrar_interesse()` ao cliente e verificar com `tests/frontend/teste_api_cliente.py`
- [x] 2.2 Criar a página "Buscar colegas" e incluí-la na navegação; verificar com `tests/frontend/teste_telas_busca.py` (lista com percentual, "Tenho interesse" vira "Interesse enviado", lista vazia orienta a completar o perfil)
