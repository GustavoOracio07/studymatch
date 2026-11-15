# Tasks

## 1. Backend (Xano)

- [x] 1.1 `meus_matches_GET.xs`: nos itens de `confirmados`, chamar `StudyMatch/calcular_compatibilidade` e incluir `disciplinas_comuns`
- [x] 1.2 Revisar com `git diff`, rodar `xano workspace push --dry-run`, publicar e alinhar com `xano workspace pull`
- [x] 1.3 `tests/api/teste_matches.py`: cobrir `disciplinas_comuns` nos confirmados (com e sem disciplina em comum) e a ausência nos pendentes

## 2. Frontend (Streamlit)

- [x] 2.1 `dominio.py`: `link_whatsapp(telefone, nome, disciplinas)` com a lista de nomes na mensagem; cobrir em `tests/frontend/teste_api_cliente.py`
- [x] 2.2 `matches.py`: traduzir `disciplinas_comuns` com `listar_disciplinas()` e passar para `link_whatsapp`
- [x] 2.3 `tests/frontend/teste_telas_matches.py`: conferir o texto da mensagem no link do botão
