# Tasks

## 1. Backend (Xano)

- [ ] 1.1 Criar `GET /meus_matches` (recebidos, enviados, confirmados; telefone só nos confirmados; ignora órfãos) e verificar com `tests/api/teste_matches.py`
- [ ] 1.2 Restringir `DELETE /match_interesse/{id}` a interesses pendentes e verificar com `tests/api/teste_matches.py`
- [ ] 1.3 Publicar com dry-run + push, alinhar o local com pull e verificar que `tests/api/teste_seguranca.py` e `tests/api/teste_busca.py` continuam passando

## 2. Frontend (Streamlit)

- [ ] 2.1 Adicionar `meus_matches()`, `responder_interesse()` e `cancelar_interesse()` ao cliente e verificar com `tests/frontend/teste_api_cliente.py`
- [ ] 2.2 Criar a página "Meus matches" (abas Recebidos, Enviados e Confirmados) e incluí-la na navegação; verificar com `tests/frontend/teste_telas_matches.py` (aceitar mostra o telefone, recusar não mostra, cancelar remove)
