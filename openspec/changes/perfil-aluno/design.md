# Design

## Context

A change `seguranca-backend-xano` já garante o dono dos registros. Faltam as regras de conteúdo. As horas são guardadas como texto (`hora_inicio`, `hora_fim`); no formato HH:MM com zeros à esquerda, a comparação de texto equivale à comparação de horário. O plano free do Xano limita a 10 requisições a cada 20 s.

## Goals / Non-Goals

**Goals:**
- Regras de domínio no Xano, reaproveitadas pelos endpoints que gravam o mesmo dado.
- Poucas requisições por ação na tela.

**Non-Goals:**
- Migrar `hora_inicio`/`hora_fim` para outro tipo de coluna.
- Validar os dados antigos já gravados (só há registros de teste).

## Decisions

1. **Funções de validação reutilizáveis** em `function/study_match/`:
   - `validar_disponibilidade(user_id, dia_semana, hora_inicio, hora_fim, ignorar_id)`: regex `^([01][0-9]|2[0-3]):[0-5][0-9]$`, fim > início e sobreposição com `db.query ... return exists` (`inicio < fim_existente && fim > inicio_existente`, no mesmo dia e com `id != ignorar_id`). Usada em POST e PATCH.
   - `validar_disciplina_do_curso(user_id, disciplina_id)`: a disciplina existe e `curso_id` é igual ao do aluno. Usada em POST e PATCH de `usuario_disciplina`.
2. **`PUT /minhas_disciplinas` substitui a lista inteira em uma transação** (apaga as atuais e insere as novas). Alternativa: a tela chamar POST/DELETE para cada diferença. Descartada porque várias chamadas estouram o limite de requisições e podem deixar a lista pela metade. O caminho fica fora de `usuario_disciplina/...` para não colidir com a rota `usuario_disciplina/{usuario_disciplina_id}`.
3. **Validação da lista:** busca as disciplinas do curso do aluno e usa `diff` entre os ids enviados e os válidos. Ids repetidos são removidos com `unique`.
4. **Troca de curso remove as disciplinas de dificuldade.** Alternativa: bloquear a troca enquanto houver disciplinas. Descartada por ser pior para o aluno. A tela avisa antes de salvar.
5. **`PATCH /auth/me` recebe o perfil completo** (a tela sempre envia todos os campos), o que evita ambiguidade entre "não enviado" e "vazio". A resposta é relida com `output` explícito, para nunca devolver o hash da senha.
6. **Na tela, as listas do aluno ficam em `st.session_state`** e só são recarregadas depois de uma alteração. O catálogo de disciplinas usa o cache de 10 min já existente.
7. **O cliente repete a chamada após um 429** (esperas de 2, 4 e 8 s) antes de mostrar o erro. Os testes de tela mostraram que abrir "Meu perfil" logo depois de outras ações estoura o limite do plano free (a página faz até 4 chamadas na primeira abertura).

## Risks / Trade-offs

- [Comparação de texto em `where`] → Só é correta com HH:MM de dois dígitos, o que a regex garante antes de gravar.
- [Troca de curso apaga dados] → Aviso explícito na tela antes de salvar.

## Migration Plan

Validar os `.xs` → `xano workspace push --dry-run` → push → testes de API (`tests/api/teste_perfil.py`) → testes de tela (`tests/frontend/teste_telas_perfil.py`) → pull para alinhar o formato local.
