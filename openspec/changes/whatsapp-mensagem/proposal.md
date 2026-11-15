# Proposal

## Why

Nos matches confirmados, o botão "Chamar no WhatsApp" abre a conversa com uma mensagem genérica ("Deu match no StudyMatch..."). O colega pode não lembrar por que deu match. Citar as disciplinas em comum deixa claro o motivo do contato e ajuda a puxar o assunto. O botão também entrou sem change no OpenSpec, então o comportamento dele ainda não está nas specs.

## What Changes

- `GET /meus_matches` passa a incluir `disciplinas_comuns` (ids) nos itens de `confirmados`, calculadas com a função `StudyMatch/calcular_compatibilidade` já existente.
- A mensagem pronta do WhatsApp passa a citar os nomes das disciplinas em comum. Exemplo: "Oi, Ana! Deu match no StudyMatch: temos dificuldade em Cálculo I e Banco de Dados. Bora marcar um horário para estudar juntos?".
- Sem disciplina em comum (o colega mudou as disciplinas depois do match), a mensagem continua a genérica.
- O botão "Chamar no WhatsApp" passa a ter requisito na spec `meus-matches`.

**Fora do escopo:**
- Chat dentro do sistema (decisão do grupo: o contato fica no WhatsApp).
- Incluir horários em comum na mensagem.
- Disciplinas em comum em `recebidos` e `enviados`.

## Capabilities

### New Capabilities
<!-- Nenhuma. -->

### Modified Capabilities
- `meus-matches`: os confirmados trazem as disciplinas em comum, e a página tem o botão do WhatsApp com mensagem pronta.

## Impact

- Xano: `api/authentication/meus_matches_GET.xs`.
- Streamlit: `studymatch/dominio.py` (`link_whatsapp`) e `paginas/matches.py`.
- Testes: `tests/api/teste_matches.py`, `tests/frontend/teste_api_cliente.py` e `tests/frontend/teste_telas_matches.py`.
