# Proposal

## Why

Com o perfil, as disciplinas e os horários preenchidos, falta o objetivo principal do StudyMatch: mostrar ao aluno quais colegas são compatíveis e deixar que ele demonstre interesse. Hoje o percentual de compatibilidade vem do cliente, então qualquer um pode inventar o número, e o interesse cruzado (A→B e depois B→A) cria dois registros em vez de virar match.

## What Changes

- Nova função de backend que calcula a compatibilidade entre dois alunos: 60% pelas disciplinas de dificuldade em comum e 40% pelos horários em comum.
- Novo `GET /compativeis`: lista os colegas com pelo menos uma disciplina de dificuldade em comum, ordenados pelo percentual. Para cada um, mostra as disciplinas e os horários em comum e a situação do interesse entre os dois. **Não expõe telefone nem e-mail.**
- **BREAKING**: `POST /match_interesse` deixa de aceitar o percentual vindo do cliente; o backend calcula. Se o outro aluno já tinha enviado interesse pendente, o registro existente vira `match` em vez de criar outro (interesse cruzado). Interesse repetido devolve mensagem amigável.
- Nova página "Buscar colegas" no Streamlit, com o percentual, as disciplinas e os horários em comum, e o botão "Tenho interesse" (ou "Aceitar interesse", quando o colega já demonstrou interesse).

**Fora do escopo:**
- Tela "Meus matches", aceite/recusa pela lista de pedidos recebidos e exibição do telefone (próxima change).
- Filtros e paginação na busca.
- Semestre no cálculo (decisão do domínio: fica fora do MVP).
- Grupos com mais de dois alunos.

## Capabilities

### New Capabilities
- `busca-compatibilidade`: cálculo do percentual de compatibilidade e a lista de colegas compatíveis.
- `interesse-match`: envio de interesse com percentual calculado no backend e a regra de interesse cruzado.

### Modified Capabilities
<!-- Nenhuma: as regras de acesso do match_interesse (controle-de-acesso) continuam como estão. -->

## Impact

- Xano: nova função `StudyMatch/calcular_compatibilidade`, novo endpoint `compativeis` (GET) e alteração de `match_interesse` (POST).
- Streamlit: nova página `paginas/buscar.py` e novos métodos no cliente.
