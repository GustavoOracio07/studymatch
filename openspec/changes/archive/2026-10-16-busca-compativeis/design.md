# Design

## Context

O domínio define "60% pelas disciplinas de dificuldade em comum e 40% pelos horários de disponibilidade em comum", sem detalhar como medir cada parte. As disciplinas são sempre do próprio curso (change `perfil-aluno`), então só alunos do mesmo curso podem ter disciplinas em comum. As faixas de um mesmo aluno não se sobrepõem, então o total de minutos é a soma simples das faixas.

## Goals / Non-Goals

**Goals:**
- Cálculo em um único lugar no backend, usado pela busca e pelo envio de interesse.
- A busca inteira em uma única requisição (limite do plano free).

**Non-Goals:**
- Guardar o percentual pré-calculado ou atualizar o percentual de interesses antigos quando os perfis mudam.
- Otimizar para muitos alunos (o MVP tem poucos usuários).

## Decisions

1. **Medida de cada parte: coeficiente de sobreposição** (em comum ÷ o menor dos dois conjuntos), para disciplinas e para minutos. Ele é simétrico e não pune quem informou muitos horários: se todos os horários de A cabem nos de B, a parte de horários é 100%. Alternativa: Jaccard (em comum ÷ união). Descartada porque derruba o percentual de quem tem agenda ampla. **É uma interpretação da regra do domínio** e pode ser ajustada só na função.
2. **Função `StudyMatch/calcular_compatibilidade(usuario_a, usuario_b)`** devolve `{percentual, disciplinas_comuns, horarios_comuns}`. Horas HH:MM são comparadas como texto para achar a interseção e convertidas em minutos (`substr` + `to_int`) para somar.
3. **Candidatos da busca:** alunos do mesmo curso (exceto o próprio). A função é aplicada a cada um, e só ficam os que têm ao menos uma disciplina em comum. Isso evita filtrar por lista de ids no `where`.
4. **Situação do interesse** vem dos registros de `Match_interesse` em que o aluno participa, com a prioridade `match` > `recebido` (pendente, ele é o alvo) > `enviado` (pendente, ele é a origem) > `recusado`. O `interesse_id` acompanha a situação para a tela poder agir.
5. **Disciplinas em comum vão como ids**; a tela traduz com o catálogo que já está em cache. Assim a busca não faz outra consulta.
6. **Interesse cruzado no `POST /match_interesse`:** procura o registro inverso (alvo → aluno do token). Se estiver `pendente`, faz `db.edit` para `match`. Se estiver `match`, responde 400. Caso contrário, segue para a criação normal, com checagem de repetição. Na tela, "Aceitar interesse" usa esse mesmo endpoint.

## Risks / Trade-offs

- [Interpretação da fórmula] → Documentada aqui e no spec; muda em um só lugar.
- [Busca faz consultas por candidato] → Aceitável para o volume do MVP; poderia virar consulta agregada depois.
- [Percentual gravado no interesse fica desatualizado se os perfis mudarem] → A busca sempre mostra o valor atual.

## Migration Plan

Validar `.xs` → dry-run → push → `tests/api/teste_busca.py` e `tests/api/teste_seguranca.py` → pull para alinhar → telas com `tests/frontend/teste_telas_busca.py`.
