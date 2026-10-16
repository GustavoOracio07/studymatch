# Design

## Context

`GET /match_interesse` devolve só os registros crus, sem dados do colega. A regra de privacidade exige que o telefone só saia do backend depois do match; por isso a montagem com os dados do colega precisa acontecer no Xano, nunca no Streamlit. O `DELETE /auth/me` não apaga os interesses do aluno (decisão da change `seguranca-backend-xano`), então podem existir registros órfãos.

## Goals / Non-Goals

**Goals:**
- Uma única requisição traz as três listas (limite do plano free).
- O telefone sai do backend só para matches confirmados.

**Non-Goals:**
- Paginação e histórico de pedidos recusados por mim.

## Decisions

1. **Endpoint dedicado `meus_matches`**, em vez de mudar o `GET /match_interesse`, para não quebrar o contrato atual nem misturar registros crus com dados de perfil.
2. **Para cada registro**, o endpoint faz `db.get user` do colega com `output` explícito (`Name`, `Sobrenome`, `Semestre`, `Sobre_mim`, `Telefone`) e monta o item. O `telefone` só entra no objeto quando `status == "match"`. Colega `null` (conta apagada) → o registro é pulado.
3. **Ações reaproveitam endpoints existentes:** `PATCH /match_interesse/{id}` para aceitar/recusar e `DELETE /match_interesse/{id}` para cancelar. O DELETE ganha a pré-condição `status == "pendente"`, porque apagar um match tiraria o contato do outro aluno sem que ele concordasse.
4. **Na tela**, as listas ficam em `st.session_state["meus_matches"]`. Depois de uma ação, a sessão é invalidada (`meus_matches` e `compativeis`) e a página recarrega, o que custa uma requisição.

## Risks / Trade-offs

- [Consulta por registro] → Aceitável para o volume do MVP.
- [Órfãos acumulam no banco] → Ficam invisíveis; limpeza pode ser feita depois.
