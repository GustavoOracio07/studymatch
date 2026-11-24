# chat-match Specification

## Purpose
Permite que os dois alunos de um match confirmado troquem mensagens de texto dentro do StudyMatch, sem que outras pessoas leiam ou enviem mensagens na conversa.

## Requirements

### Requirement: Enviar mensagem
`POST /mensagem` SHALL gravar uma mensagem com `match_interesse_id` e `texto`, usando o aluno do token como remetente e ignorando qualquer remetente enviado pelo cliente. O texto, sem espaços nas pontas, SHALL ter de 1 a 500 caracteres. A resposta SHALL ter `id`, `remetente_id`, `texto` e `created_at`.

#### Scenario: Envio válido
- **WHEN** A, que tem match confirmado com B, envia "Oi!"
- **THEN** o sistema responde 200 e a mensagem fica gravada com A como remetente

#### Scenario: Remetente forjado
- **WHEN** A envia uma mensagem informando o id de B como remetente
- **THEN** a mensagem é gravada com A como remetente

#### Scenario: Texto vazio
- **WHEN** A envia um texto vazio ou só com espaços
- **THEN** o sistema responde 400 e nada é gravado

#### Scenario: Texto longo demais
- **WHEN** A envia um texto com 501 caracteres
- **THEN** o sistema responde 400 e nada é gravado

### Requirement: Ler a conversa
`GET /mensagem` SHALL devolver, da mais antiga para a mais nova, as mensagens do `match_interesse_id` informado, com `id`, `remetente_id`, `texto` e `created_at`. Sem `depois_de`, SHALL devolver as 50 últimas. Com `depois_de`, SHALL devolver no máximo as 50 primeiras mensagens com id maior que ele.

#### Scenario: Abrir a conversa
- **WHEN** A e B trocaram mensagens e B consulta a conversa sem `depois_de`
- **THEN** B recebe as mensagens dos dois em ordem

#### Scenario: Só as novas
- **WHEN** B consulta com `depois_de` igual ao id da primeira de duas mensagens
- **THEN** a resposta traz apenas a segunda

#### Scenario: Nenhuma mensagem nova
- **WHEN** B consulta com `depois_de` igual ao id da última mensagem
- **THEN** o sistema responde 200 com uma lista vazia

### Requirement: Conversa restrita aos alunos do match
Enviar e ler SHALL exigir token válido, que o aluno participe do match e que o status seja `match`.

#### Scenario: Aluno de fora do match
- **WHEN** C, que não participa do match entre A e B, tenta ler ou enviar
- **THEN** o sistema responde 403 e nada é gravado

#### Scenario: Interesse não confirmado
- **WHEN** A tenta ler ou enviar em um interesse `pendente` ou `recusado` do qual participa
- **THEN** o sistema responde 403 e nada é gravado

#### Scenario: Match inexistente
- **WHEN** A tenta ler ou enviar em um match que não existe
- **THEN** o sistema responde 404

#### Scenario: Sem token
- **WHEN** um cliente tenta ler ou enviar sem token
- **THEN** o sistema responde 401

### Requirement: Página Conversa
O app SHALL ter uma página de conversa com um cabeçalho do colega (foto ou iniciais, nome completo e disciplinas em comum, se houver), as mensagens em balões e um campo de envio. As mensagens do aluno SHALL ficar à direita e as do colega à esquerda, com a foto dele, e cada uma SHALL mostrar a hora de Brasília, com a data quando não for de hoje. Enquanto aberta, ela SHALL buscar mensagens novas a cada 8 segundos. O texto SHALL ser mostrado literalmente, sem interpretar HTML ou Markdown.

#### Scenario: Enviar pela tela
- **WHEN** A envia "Oi!" pela página
- **THEN** a mensagem aparece na conversa de A

#### Scenario: Enviar com a busca no limite
- **WHEN** o envio de A é aceito, mas as buscas estão falhando pelo limite do Xano
- **THEN** a mensagem enviada aparece na conversa de A mesmo assim

#### Scenario: Nome do autor
- **WHEN** A vê a conversa com Ana
- **THEN** as mensagens de A aparecem à direita e as de Ana à esquerda, com a foto ou as iniciais dela

#### Scenario: Colega sem foto
- **WHEN** A abre a conversa com um colega sem foto
- **THEN** o cabeçalho e os balões do colega mostram as iniciais dele

#### Scenario: Hora da mensagem
- **WHEN** A vê uma mensagem enviada hoje às 18:38 de Brasília
- **THEN** o balão mostra "18:38"

#### Scenario: Receber mensagem
- **WHEN** B está com a conversa aberta e A envia uma mensagem, sem erro de rede nem de limite
- **THEN** a mensagem aparece para B na próxima busca, sem recarregar a página

#### Scenario: Texto com HTML
- **WHEN** A envia `<b>oi</b>`
- **THEN** B vê o texto `<b>oi</b>` e não a palavra em negrito

#### Scenario: Limite de requisições
- **WHEN** uma busca automática falha pelo limite do Xano
- **THEN** a tela mostra o aviso discreto "Atualizando a conversa...", mantém as mensagens já carregadas e tenta de novo na busca seguinte

#### Scenario: Sem conversa escolhida
- **WHEN** o aluno abre a página sem ter escolhido um match
- **THEN** a página pede para escolher um colega em Meus matches
