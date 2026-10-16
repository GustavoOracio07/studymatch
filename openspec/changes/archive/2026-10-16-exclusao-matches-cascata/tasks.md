# Tasks

## 1. Backend (Xano)

- [x] 1.1 Incluir em `StudyMatch/excluir_usuario` o `db.bulk.delete` de `Match_interesse` (origem ou alvo) na mesma transação; verificar com o validador do XanoScript e `xano workspace push --dry-run`
- [x] 1.2 Publicar com `xano workspace push`, alinhar o local com `xano workspace pull` e verificar com `tests/api/teste_matches.py` que match, pedido enviado e pedido recebido somem para os outros alunos
- [x] 1.3 Rodar `tests/api/teste_seguranca.py` e verificar que a exclusão da conta continua funcionando

## 2. Frontend (Streamlit)

- [x] 2.1 Nenhuma alteração; verificar que `git diff` não toca em arquivos Python fora de `tests/`
