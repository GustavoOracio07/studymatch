# Spec Delta

## MODIFIED Requirements

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
