# Tasks

## 1. Backend (Xano)

- [x] 1.1 Criar `table/mensagem.xs` com índice em `match_interesse_id` + `id`; conferir com `xano workspace push --dry-run`
- [x] 1.2 Criar `mensagem_POST.xs` e `mensagem_GET.xs` com as regras de acesso e validação; conferir com `--dry-run`
- [x] 1.3 Apagar as mensagens em `excluir_usuario.xs`, dentro da transação; conferir com `git diff`
- [x] 1.4 Criar `tests/api/teste_chat.py` com os cenários de envio, leitura, acesso e exclusão; conferir que ele executa
- [x] 1.5 Publicar no Xano com a aprovação do usuário e alinhar com `xano workspace pull`; verificar que `teste_chat.py`, `teste_matches.py` e `teste_seguranca.py` passam
- [x] 1.6 Atualizar `docs/domain-model.md` e `docs/project-overview.md` (chat, tabela e escopo); conferir que não dizem mais que não há chat

## 2. Frontend (Streamlit)

- [x] 2.1 `api.py`: `enviar_mensagem` e `mensagens`, com busca sem novas tentativas; cobrir em `teste_api_cliente.py` e verificar que passa
- [x] 2.2 Criar `paginas/conversa.py` e registrar em `app.py`; verificar envio, recebimento e texto literal em `teste_telas_chat.py`
- [x] 2.3 `matches.py`: botão "Conversar" em Confirmados; verificar que `teste_telas_chat.py` e `teste_telas_matches.py` passam
- [x] 2.4 Citar o chat e a limitação no `README.md`; conferir que os testes novos estão na lista

## 3. Integração

- [x] 3.1 Abrir duas contas no app local e trocar mensagens; verificar que chegam sem recarregar e conferir os temas claro e escuro
