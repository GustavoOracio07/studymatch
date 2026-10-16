# Spec Delta

## MODIFIED Requirements

### Requirement: Exclusão em cascata do usuário
O aluno SHALL poder apagar a própria conta com `DELETE /auth/me`, e o sistema SHALL apagar junto, na mesma transação, as disponibilidades, as disciplinas de dificuldade e todos os interesses de match em que ele é origem ou alvo, em qualquer status.

#### Scenario: Aluno apaga a própria conta
- **WHEN** um aluno com disponibilidades e disciplinas de dificuldade chama `DELETE /auth/me`
- **THEN** o sistema responde 200, o login dele passa a falhar e não resta nenhum registro de `disponibilidade` nem de `usuario_disciplina` com o `usuario_id` dele

#### Scenario: Interesses de match do aluno apagado
- **WHEN** o aluno A tem um match confirmado com B, um interesse pendente enviado para C e um interesse recebido de D, e A chama `DELETE /auth/me`
- **THEN** os três registros de `match_interesse` são apagados e não aparecem mais em `GET /match_interesse` de B, C e D

#### Scenario: Exclusão sem token
- **WHEN** um cliente chama `DELETE /auth/me` sem token
- **THEN** o sistema responde 401 e nada é apagado
