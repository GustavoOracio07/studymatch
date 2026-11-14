# Spec Delta

## MODIFIED Requirements

### Requirement: Foto de perfil
O aluno SHALL poder enviar, trocar e remover a própria foto de perfil. O frontend SHALL reduzir a imagem escolhida (JPEG, PNG ou WEBP de até 2 MB) para 256x256 em JPEG e enviá-la como data URL no campo `foto`. O sistema SHALL aceitar apenas data URLs que comecem com `data:image/jpeg;base64,` e tenham até 300 mil caracteres, SHALL guardar a foto no próprio registro do aluno (sem o armazenamento de imagens do Xano, que aplica marca d'água) e SHALL devolver `foto_url` no perfil (`null` quando não houver foto).

#### Scenario: Enviar foto válida
- **WHEN** um aluno sem foto envia pela tela uma imagem PNG
- **THEN** o sistema responde 200 com o perfil, e `foto_url` é uma data URL JPEG de 256x256, sem marca d'água

#### Scenario: Trocar a foto
- **WHEN** um aluno que já tem foto envia outra imagem válida
- **THEN** `foto_url` passa a ser a nova foto e, se a anterior era um arquivo do armazenamento, ele é apagado

#### Scenario: Conteúdo que não é imagem JPEG
- **WHEN** um aluno chama `POST /auth/me/foto` com `foto` = `data:application/pdf;base64,...`
- **THEN** o sistema responde 400 com a mensagem "Envie uma imagem JPEG, PNG ou WEBP." e a foto atual não muda

#### Scenario: Foto grande demais
- **WHEN** um aluno envia uma data URL com mais de 300 mil caracteres
- **THEN** o sistema responde 400 com a mensagem "A foto é grande demais." e a foto atual não muda

#### Scenario: Envio sem foto
- **WHEN** um aluno chama `POST /auth/me/foto` sem o campo `foto`
- **THEN** o sistema responde 400 e a foto atual não muda

#### Scenario: Remover a foto
- **WHEN** um aluno com foto chama `DELETE /auth/me/foto`
- **THEN** o sistema responde 200 e `GET /auth/me` devolve `foto_url` nulo

#### Scenario: Sem token
- **WHEN** um cliente chama `POST /auth/me/foto` ou `DELETE /auth/me/foto` sem token
- **THEN** o sistema responde 401 e nenhuma foto é alterada
