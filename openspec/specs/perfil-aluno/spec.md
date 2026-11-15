# perfil-aluno Specification

## Purpose
Permite que o aluno mantenha o próprio perfil, as disciplinas em que tem dificuldade e os horários disponíveis, que são a base para calcular a compatibilidade com outros alunos.

## Requirements

### Requirement: Consultar o próprio perfil
`GET /auth/me` SHALL devolver id, nome, sobrenome, e-mail, curso, semestre, telefone e sobre mim do aluno do token, e SHALL NOT devolver a senha.

#### Scenario: Aluno consulta o perfil
- **WHEN** o aluno chama `GET /auth/me` com token válido
- **THEN** a resposta contém `Name`, `Sobrenome`, `email`, `curso_id`, `Semestre`, `Telefone` e `Sobre_mim`, e não contém `Password`

### Requirement: Editar o próprio perfil
`PATCH /auth/me` SHALL atualizar nome, sobrenome, telefone, curso, semestre e sobre mim do aluno do token, com as mesmas regras do cadastro.

#### Scenario: Edição válida
- **WHEN** o aluno envia `PATCH /auth/me` com dados válidos
- **THEN** o sistema responde 200 com o perfil atualizado, sem a senha

#### Scenario: Semestre fora do intervalo
- **WHEN** o aluno envia `semestre = 13`
- **THEN** o sistema responde 400 com "O semestre deve estar entre 1 e 12" e nada muda

#### Scenario: Telefone de outro aluno
- **WHEN** o aluno envia um telefone que pertence a outro aluno
- **THEN** o sistema responde 400 com "Este telefone já está cadastrado." e nada muda

#### Scenario: Troca de curso
- **WHEN** o aluno troca o curso
- **THEN** as disciplinas de dificuldade dele são removidas, porque eram do curso anterior

### Requirement: Disciplinas de dificuldade só do próprio curso
O aluno SHALL poder escolher apenas disciplinas do próprio curso, sem repetir disciplina.

#### Scenario: Definir a lista de disciplinas
- **WHEN** o aluno envia `PUT /minhas_disciplinas` com disciplinas do próprio curso
- **THEN** a lista de disciplinas de dificuldade dele passa a ser exatamente essa

#### Scenario: Disciplina de outro curso na lista
- **WHEN** a lista enviada contém uma disciplina de outro curso
- **THEN** o sistema responde 400 com "Escolha apenas disciplinas do seu curso." e a lista anterior continua igual

#### Scenario: Adicionar disciplina de outro curso
- **WHEN** o aluno chama `POST /usuario_disciplina` com uma disciplina de outro curso
- **THEN** o sistema responde 400 com "Escolha apenas disciplinas do seu curso."

#### Scenario: Disciplina repetida
- **WHEN** o aluno chama `POST /usuario_disciplina` com uma disciplina que já está na lista dele
- **THEN** o sistema responde 400 com "Esta disciplina já está na sua lista."

### Requirement: Disponibilidade válida e sem sobreposição
Cada faixa de disponibilidade SHALL ter horas em HH:MM (00:00 a 23:59), fim depois do início e nenhuma sobreposição com outra faixa do mesmo aluno no mesmo dia. Faixas que só se encostam são permitidas.

#### Scenario: Faixa válida
- **WHEN** o aluno cadastra segunda das 09:00 às 11:00 e depois segunda das 11:00 às 13:00
- **THEN** as duas faixas são criadas

#### Scenario: Faixa sobreposta
- **WHEN** o aluno já tem segunda das 09:00 às 11:00 e cadastra segunda das 10:00 às 12:00
- **THEN** o sistema responde 400 com "Este horário se sobrepõe a outra disponibilidade sua." e nada é gravado

#### Scenario: Formato inválido
- **WHEN** o aluno envia `hora_inicio = "9h"`
- **THEN** o sistema responde 400 com "Use horários no formato HH:MM."

#### Scenario: Atravessar a meia-noite
- **WHEN** o aluno envia início 23:00 e fim 01:00
- **THEN** o sistema responde 400 com "O horário de fim deve ser depois do horário de início"

#### Scenario: Editar sem conflitar consigo mesma
- **WHEN** o aluno edita uma faixa trocando só o horário de fim
- **THEN** a faixa não é considerada sobreposta a ela mesma

### Requirement: Página Meu perfil
O app SHALL ter a página "Meu perfil", com as abas Dados, Disciplinas e Disponibilidade, que usa os endpoints acima e mostra os erros da API.

#### Scenario: Escolher disciplinas
- **WHEN** o aluno abre a aba Disciplinas
- **THEN** só aparecem as disciplinas do curso dele e, ao salvar, a lista é enviada para `PUT /minhas_disciplinas`

#### Scenario: Cadastrar disponibilidade sobreposta
- **WHEN** o aluno adiciona uma faixa que se sobrepõe a outra
- **THEN** a página mostra "Este horário se sobrepõe a outra disponibilidade sua."

### Requirement: Foto de perfil
O aluno SHALL poder enviar, trocar e remover a própria foto de perfil. O frontend SHALL reduzir a imagem escolhida (JPEG, PNG ou WEBP de até 2 MB) para 256x256 em JPEG e enviá-la como data URL no campo `foto`. O sistema SHALL aceitar apenas data URLs que comecem com `data:image/jpeg;base64,` e tenham até 300 mil caracteres, SHALL guardar a foto no próprio registro do aluno (sem o armazenamento de imagens do Xano, que aplica marca d'água) e SHALL devolver `foto_url` no perfil (`null` quando não houver foto).

#### Scenario: Enviar foto válida
- **WHEN** um aluno sem foto envia pela tela uma imagem PNG
- **THEN** o sistema responde 200 com o perfil, e `foto_url` é uma data URL JPEG de 256x256, sem marca d'água

#### Scenario: Trocar a foto
- **WHEN** um aluno que já tem foto envia outra imagem válida
- **THEN** `foto_url` passa a ser a nova foto e, se a anterior era um arquivo do armazenamento, ele é apagado

#### Scenario: Arquivo que não é imagem
- **WHEN** um aluno chama `POST /auth/me/foto` com `foto` = `data:application/pdf;base64,...`
- **THEN** o sistema responde 400 com a mensagem "Envie uma imagem JPEG, PNG ou WEBP." e a foto atual não muda

#### Scenario: Imagem grande demais
- **WHEN** um aluno envia uma data URL com mais de 300 mil caracteres
- **THEN** o sistema responde 400 com a mensagem "A foto é grande demais." e a foto atual não muda

#### Scenario: Envio sem arquivo
- **WHEN** um aluno chama `POST /auth/me/foto` sem o campo `foto`
- **THEN** o sistema responde 400 e a foto atual não muda

#### Scenario: Remover a foto
- **WHEN** um aluno com foto chama `DELETE /auth/me/foto`
- **THEN** o sistema responde 200 e `GET /auth/me` devolve `foto_url` nulo

#### Scenario: Remover sem ter foto
- **WHEN** um aluno sem foto chama `DELETE /auth/me/foto`
- **THEN** o sistema responde 200 e nada muda

#### Scenario: Sem token
- **WHEN** um cliente chama `POST /auth/me/foto` ou `DELETE /auth/me/foto` sem token
- **THEN** o sistema responde 401 e nenhuma foto é alterada

### Requirement: Foto na página Meu perfil
A aba "Dados" da página Meu perfil SHALL mostrar a foto atual (ou um avatar com as iniciais) e SHALL permitir enviar uma nova foto e remover a atual.

#### Scenario: Enviar foto pela tela
- **WHEN** o aluno escolhe uma imagem PNG no seletor de arquivo e clica em "Salvar foto"
- **THEN** a tela mostra "Foto salva." e o avatar passa a exibir a nova imagem

#### Scenario: Remover foto pela tela
- **WHEN** o aluno com foto clica em "Remover foto"
- **THEN** a tela mostra o avatar com as iniciais do nome e sobrenome

#### Scenario: Erro de validação pela tela
- **WHEN** o Xano recusa a imagem enviada
- **THEN** a tela mostra a mensagem de erro do Xano e mantém a foto anterior
