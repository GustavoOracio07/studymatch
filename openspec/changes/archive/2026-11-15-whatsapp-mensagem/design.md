# Design

## Context

O `GET /meus_matches` devolve os dados do colega, mas não as disciplinas. As disciplinas de outro aluno não são públicas: só a interseção com as do aluno do token aparece, em `GET /compativeis`. A função `StudyMatch/calcular_compatibilidade` já devolve `disciplinas_comuns`.

## Goals / Non-Goals

**Goals:**
- Mensagem do WhatsApp com os nomes das disciplinas em comum.
- Reaproveitar o cálculo que já existe no Xano.

**Non-Goals:**
- Mudar o percentual guardado no interesse ou recalcular a compatibilidade nas outras listas.

## Decisions

- **Interseção calculada no Xano, só para `confirmados`.** O frontend não pode calcular sozinho, porque não tem acesso às disciplinas do colega. Calcular só nos confirmados evita trabalho extra nas outras listas. A função roda dentro do endpoint, então não conta no limite de requisições do plano free.
- **Ids no backend, nomes no frontend.** Mesmo formato de `GET /compativeis`: o endpoint devolve ids e a tela traduz com `listar_disciplinas()`, que já fica em cache.
- **Montagem da mensagem em `link_whatsapp`.** A função ganha o parâmetro opcional `disciplinas` (lista de nomes). Duas disciplinas ficam "A e B"; três ou mais, "A, B e C".

## Risks / Trade-offs

- Uma chamada a `calcular_compatibilidade` por match confirmado deixa o endpoint um pouco mais lento. Com poucos matches por aluno, o impacto é pequeno.
- Mensagens muito longas, se houver muitas disciplinas em comum. Aceitável: o aluno pode editar a mensagem no WhatsApp antes de enviar.
