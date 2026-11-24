# Proposal

## Why

A conversa do match usa o visual padrão do Streamlit: não há foto do colega nem diferença clara entre as mensagens dos dois alunos. Ela será mostrada no vídeo da apresentação (27/11/2026) e precisa ser fácil de entender.

## What Changes

- Cabeçalho com foto (ou iniciais), nome completo e disciplinas em comum.
- Mensagens em balões: as do aluno à direita, as do colega à esquerda com a foto, todas com a hora no lugar do nome do autor.
- Campo de envio com o nome do colega e botão roxo.
- Modos claro e escuro.

**Fora do escopo:** indicador de online (o sistema não tem essa informação), confirmação de leitura e qualquer mudança no Xano ou na busca de mensagens.

## Capabilities

### Modified Capabilities
- `chat-match`: a Página Conversa identifica o autor pelo lado do balão, mostra a hora e traz os dados do colega no cabeçalho.

## Impact

- Streamlit: `paginas/conversa.py`, `paginas/matches.py`, `studymatch/visual.py`, `assets/estilo.css` e `assets/estilo_escuro.css`.
- Testes: `tests/frontend/teste_telas_chat.py`.
