# Proposal

## Why

A sugestão de colegas depende das disciplinas em que o aluno tem dificuldade e dos horários livres dele, mas hoje não há tela para informar esses dados nem para corrigir o cadastro. As regras do domínio também ainda não valem no backend: a disciplina tem que ser do próprio curso, o horário tem que estar em HH:MM e as faixas do mesmo aluno não podem se sobrepor.

## What Changes

- `GET /auth/me` passa a devolver o perfil completo do próprio aluno (sobrenome, curso, semestre, telefone e sobre mim).
- Novo `PATCH /auth/me`: o aluno edita nome, sobrenome, telefone, curso, semestre e sobre mim. Vale o semestre de 1 a 12, o telefone único (com mensagem amigável) e o curso existente.
- Ao trocar de curso, as disciplinas de dificuldade do curso anterior são removidas, porque deixam de ser válidas.
- Novo `PUT /minhas_disciplinas`: substitui de uma vez a lista de disciplinas de dificuldade do aluno. Todas precisam ser do curso dele.
- `POST`/`PATCH /usuario_disciplina` passam a recusar disciplina de outro curso e disciplina repetida, com mensagem amigável.
- `POST`/`PATCH /disponibilidade` passam a exigir HH:MM (00:00 a 23:59), fim depois do início (sem atravessar a meia-noite) e nenhuma sobreposição com outra faixa do mesmo aluno no mesmo dia. Faixas que só se encostam, como 09:00–11:00 e 11:00–13:00, são permitidas.
- Nova página "Meu perfil" no Streamlit, com as abas Dados, Disciplinas e Disponibilidade.

**Fora do escopo:**
- Troca de e-mail e de senha.
- Foto de perfil.
- Busca de compatíveis e matches (próximas changes).

## Capabilities

### New Capabilities
- `perfil-aluno`: edição dos dados do aluno, escolha das disciplinas de dificuldade e cadastro de disponibilidade, com as regras do domínio.

### Modified Capabilities
<!-- Nenhuma: os requisitos existentes de controle de acesso continuam valendo como estão. -->

## Impact

- Xano: `auth/me` (GET), novos `auth/me` (PATCH) e `minhas_disciplinas` (PUT), endpoints de `disponibilidade` e `usuario_disciplina`, e novas funções de validação em `function/study_match/`.
- Streamlit: nova página `paginas/perfil.py` e novos métodos em `studymatch/api.py`.
