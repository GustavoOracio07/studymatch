# Proposal

## Why

O `DELETE /auth/me` apaga as disponibilidades e as disciplinas do aluno, mas não os registros de `Match_interesse` em que ele é origem ou alvo. Esses registros ficam órfãos no banco: apontam para um usuário que não existe mais. Hoje o `GET /meus_matches` só os esconde.

## What Changes

- A função `StudyMatch/excluir_usuario`, usada pelo `DELETE /auth/me`, passa a apagar também, na mesma transação, todos os `Match_interesse` em que o usuário é origem (`usuario_id`) ou alvo (`usuario_alvo_id`), em qualquer status.
- Com isso, o pedido ou o match some também para o outro aluno.

**Fora do escopo:**
- Limpar os registros órfãos que já existem. Eles pertencem a usuários apagados, então ninguém tem token para removê-los pela API; a limpeza é feita pelo painel do Xano.
- Cascata para exclusões feitas direto pelo painel (o plano free não tem triggers).

## Capabilities

### New Capabilities
<!-- Nenhuma. -->

### Modified Capabilities
- `controle-de-acesso`: a exclusão em cascata do usuário passa a incluir os interesses de match.

## Impact

- Xano: `function/study_match/excluir_usuario.xs`.
- Testes: `tests/api/teste_matches.py`.
