# Spec Delta

## MODIFIED Requirements

### Requirement: Regras de acesso do interesse de match
No `match_interesse`, o sistema SHALL permitir que apenas o aluno alvo altere o status, apenas de `pendente` para `match` ou `recusado`, e que apenas o aluno de origem apague o interesse, e somente enquanto ele estiver `pendente`. Um aluno SHALL NOT criar interesse em si mesmo.

#### Scenario: Alvo aceita o interesse
- **WHEN** o aluno alvo chama `PATCH /match_interesse/{id}` com `status = "match"` em um interesse pendente
- **THEN** o status passa para `match`

#### Scenario: Origem tenta aceitar o próprio interesse
- **WHEN** o aluno de origem chama `PATCH /match_interesse/{id}` com `status = "match"`
- **THEN** o sistema responde 403 e o status não muda

#### Scenario: Interesse em si mesmo
- **WHEN** o aluno chama `POST /match_interesse` com `usuario_alvo_id` igual ao próprio id
- **THEN** o sistema responde 400 e nada é gravado

#### Scenario: Origem cancela interesse pendente
- **WHEN** o aluno de origem chama `DELETE /match_interesse/{id}` em um interesse pendente
- **THEN** o sistema responde 200 e o interesse é apagado

#### Scenario: Origem tenta desfazer match confirmado
- **WHEN** o aluno de origem chama `DELETE /match_interesse/{id}` em um interesse com status `match`
- **THEN** o sistema responde 400 com "Só é possível cancelar interesses pendentes." e o match continua existindo
