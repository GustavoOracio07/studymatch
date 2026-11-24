# Proposal

## Why

Depois do match, o contato só acontece fora do sistema, pelo WhatsApp. Uma conversa simples dentro do StudyMatch permite mostrar a jornada completa no vídeo da apresentação (27/11/2026). Esta change revê a decisão anterior de não ter chat.

## What Changes

- Nova tabela `mensagem` e endpoints `POST /mensagem` e `GET /mensagem`, restritos aos dois alunos de um match confirmado.
- Nova página "Conversa", aberta pelo botão "Conversar" em Confirmados, que busca mensagens novas a cada 8 segundos.
- A exclusão da conta apaga também as mensagens das conversas do aluno.
- O botão "Chamar no WhatsApp" e o telefone continuam como estão.
- `docs/project-overview.md`, `docs/domain-model.md` e `README.md` passam a citar o chat e a limitação de uso do plano free do Xano.

**Fora do escopo:**
- Tempo real (WebSocket), notificações, contador de não lidas e confirmação de leitura.
- Editar ou apagar mensagens, anexos, imagens e grupos.
- Carregar mensagens anteriores às 50 últimas.
- Bloquear ou denunciar colegas.

## Capabilities

### New Capabilities
- `chat-match`: envio, leitura e tela da conversa entre os dois alunos de um match confirmado.

### Modified Capabilities
- `controle-de-acesso`: a exclusão em cascata do usuário inclui as mensagens.
- `meus-matches`: os matches confirmados ganham o botão "Conversar".

## Impact

- Xano: `table/mensagem.xs`, `api/authentication/mensagem_POST.xs`, `api/authentication/mensagem_GET.xs` e `function/study_match/excluir_usuario.xs`.
- Streamlit: `studymatch/api.py`, `paginas/conversa.py`, `paginas/matches.py` e `app.py`.
- Testes: `tests/api/teste_chat.py`, `tests/frontend/teste_telas_chat.py` e `tests/frontend/teste_api_cliente.py`.
