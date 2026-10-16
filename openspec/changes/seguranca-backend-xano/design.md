# Design

## Context

Os endpoints CRUD foram gerados automaticamente pelo Xano com `dblink` (o input espelha a tabela inteira, inclusive `usuario_id`) e sem `auth`. A tabela `user` usa os campos `Name` e `Password` com maiúscula, mas o login pede `name`/`password` no `output`, o que quebra a verificação da senha. O `event_log` recebe o registro completo do usuário como `metadata`.

O workspace local (`./xano`) foi conferido contra o remoto com `xano workspace pull` antes da change: estavam idênticos.

## Goals / Non-Goals

**Goals:**
- Toda regra de acesso fica no Xano; o Streamlit não precisa (nem consegue) burlar.
- Manter os mesmos caminhos de endpoint para não criar uma API paralela.

**Non-Goals:**
- Regras de validação de negócio (HH:MM, sobreposição, curso da disciplina), que ficam para a change de perfil.
- Middleware ou RBAC genérico.

## Decisions

1. **Inputs explícitos no lugar de `dblink`.** Os endpoints de escrita passam a declarar só os campos que o cliente pode enviar. O `usuario_id` vem de `$auth.id`. Alternativa: manter `dblink` e sobrescrever `usuario_id`. Descartada porque deixaria o cliente mandar campos inesperados (como `status` na criação do match).
2. **Verificação de dono com `db.get` + `precondition` (`accessdenied`, 403).** Um registro inexistente devolve 404 antes da checagem de dono. Esse é o padrão "Resource Ownership Check" da documentação do XanoScript.
3. **Escrita de curso/disciplina restrita a `admin` com a função existente `Quick Start/enforce_role`.** Alternativa: apagar esses endpoints do workspace. Descartada por exigir `push --sync --delete`, que é destrutivo. Com a trava de papel, o resultado prático é o mesmo ("ninguém edita pelo app"), e a manutenção continua pelo painel.
4. **Cascata com `table_trigger` na tabela `user` (ação `delete`)**, usando `db.bulk.delete` em `Disponibilidade` e `Usuario_disciplina`. O trigger cobre exclusões feitas pelo painel do Xano, que é hoje o único jeito de apagar usuário. Os registros de `Match_interesse` não entram na cascata (não foi pedido). As consultas de matches das próximas changes devem ignorar registros cujo outro aluno não existe mais.
5. **Metadata do log:** apenas `{email}` no login/cadastro e `{}` nas rotas de redefinição de senha.
6. **Mensagens amigáveis de duplicidade:** checar `email` e `Telefone` com `db.has` antes do `db.add` e responder `inputerror` (400) em português. O índice único continua como proteção final.

## Risks / Trade-offs

- [Mudança de contrato nos endpoints] → Ainda não há frontend consumindo; a change 2 já usa o novo contrato.
- [Logs antigos com hash continuam no `event_log`] → Fica registrado como ação manual (limpar ou truncar a tabela pelo painel).
- [Trigger pode não rodar em testes isolados] → Validar também chamando o trigger diretamente em um workflow test.

## Migration Plan

1. Validar os `.xs` com o validador oficial do XanoScript.
2. `xano workspace push --dry-run` e revisão da prévia.
3. `xano workspace push` (modo parcial, só arquivos alterados).
4. Testar com `curl` contra a API live (roteiro em `tasks.md`).
5. Rollback: `git revert` do commit e novo `xano workspace push`.
