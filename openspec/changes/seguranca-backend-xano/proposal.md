# Proposal

## Why

Hoje quase todos os endpoints do Xano são públicos: qualquer pessoa, sem login, consegue criar, editar ou apagar disponibilidades, disciplinas de dificuldade, interesses de match e até cursos e disciplinas, inclusive em nome de outro aluno. Além disso, o login e o cadastro gravam o hash da senha no `event_log`, o login está quebrado (`Unable to locate var: user.password`) e um telefone duplicado devolve um erro técnico. Isso precisa ser resolvido antes de construir o frontend em cima da API.

## What Changes

- Exigir token (`auth = "user"`) em todos os endpoints que leem dados pessoais ou alteram dados.
- **BREAKING**: o dono dos registros passa a ser sempre o usuário do token. Os campos `usuario_id` enviados pelo cliente em `disponibilidade`, `usuario_disciplina` e `match_interesse` são ignorados.
- **BREAKING**: as listagens `GET /disponibilidade`, `GET /usuario_disciplina` e `GET /match_interesse` passam a devolver apenas os registros do usuário autenticado (no match, aqueles em que ele é origem ou alvo).
- Edição e exclusão só são permitidas ao dono do registro. No `match_interesse`, só o aluno alvo pode mudar o status (de `pendente` para `match` ou `recusado`), e só o aluno de origem pode apagar o interesse.
- **BREAKING**: os endpoints de escrita de `curso` e `disciplina` passam a exigir usuário com papel `admin`. Os alunos (`member`) não editam esses dados pelo app; a manutenção é feita pelo painel do Xano. A leitura continua pública.
- Corrigir o login (nomes dos campos `Name`/`Password`) e não gravar mais o hash da senha no `event_log` (login, cadastro, redefinição de senha e magic link).
- Cadastro com telefone ou e-mail já usado devolve uma mensagem amigável em português.
- Ao apagar um usuário, apagar em cascata as disponibilidades e as disciplinas de dificuldade dele.
- `POST /message/send_welcome_email` passa a exigir login e só envia para o próprio usuário.

**Fora do escopo:**
- Validação de formato HH:MM, de sobreposição de horários e de disciplina do próprio curso (ficam para a change de perfil).
- Cálculo de compatibilidade no backend e regra de interesse cruzado (change de busca/matches).
- Endpoint de edição do perfil do aluno.
- Limpeza dos registros antigos do `event_log` que já contêm hash de senha.
- Recuperação de senha por e-mail (fora do escopo do MVP; só o vazamento no log é corrigido).

## Capabilities

### New Capabilities
- `autenticacao`: cadastro e login de alunos, mensagens de erro e registro de eventos sem dados sensíveis.
- `controle-de-acesso`: quem pode ler, criar, editar e apagar cada tipo de registro, e a exclusão em cascata ao apagar um usuário.

### Modified Capabilities
<!-- Nenhuma: ainda não há specs consolidadas. -->

## Impact

- Arquivos XanoScript em `xano/api/authentication/**`, novo trigger em `xano/table/trigger/`.
- Publicação no workspace do Xano com `xano workspace push`.
- Clientes da API precisam enviar `Authorization: Bearer <token>` nos endpoints protegidos. Não há frontend consumindo a API ainda, então não há quebra prática.
