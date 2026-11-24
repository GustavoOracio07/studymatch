# Design

## Context

Motivação em `proposal.md`. `GET /meus_matches` já devolve foto, sobrenome e disciplinas em comum, e `GET /mensagem` já devolve `created_at`.

## Goals / Non-Goals

**Goals:** conversa legível nos dois temas, sem novas requisições ao Xano.

**Non-Goals:** mudar o envio ou a busca de mensagens.

## Decisions

- **Balões em `st.html` com texto escapado.** O HTML não passa pelo Markdown, então o texto continua literal. Alternativa: `st.chat_message`, que não permite alinhar por autor sem depender da estrutura interna do Streamlit.
- **Foto do colega em um único estilo.** Cada balão só usa a classe, para não repetir a imagem em cada mensagem.
- **Dados do cabeçalho vêm de Meus matches pela sessão.** Não gasta requisições.
- **Hora de Brasília (UTC-3).** O servidor roda em UTC. Mensagens de outro dia mostram também a data.
- **Autor em texto oculto.** Leitores de tela continuam sabendo quem escreveu.

## Risks / Trade-offs

- [As disciplinas do cabeçalho só mudam ao reabrir a conversa] → aceitável, é só apresentação.
