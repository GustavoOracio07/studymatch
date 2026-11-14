# Spec Delta

## ADDED Requirements

### Requirement: Foto de perfil
O aluno SHALL poder enviar, trocar e remover a própria foto de perfil. O sistema SHALL aceitar apenas imagens JPEG, PNG ou WEBP de até 2 MB, SHALL deixar de referenciar a foto substituída ou removida, SHALL pedir a exclusão do arquivo com `storage.delete_file` e SHALL devolver `foto_url` no perfil (`null` quando não houver foto).

#### Scenario: Enviar foto válida
- **WHEN** um aluno sem foto chama `POST /auth/me/foto` com uma imagem PNG de 500 KB no campo `foto`
- **THEN** o sistema responde 200 com o perfil, e `foto_url` é uma URL que abre a imagem enviada

#### Scenario: Trocar a foto
- **WHEN** um aluno que já tem foto envia outra imagem válida
- **THEN** `foto_url` passa a apontar para a nova imagem e o perfil não referencia mais a foto anterior

#### Scenario: Arquivo que não é imagem
- **WHEN** um aluno envia um arquivo PDF no campo `foto`
- **THEN** o sistema responde 400 com a mensagem "Envie uma imagem JPEG, PNG ou WEBP." e a foto atual não muda

#### Scenario: Imagem grande demais
- **WHEN** um aluno envia uma imagem JPEG de 3 MB
- **THEN** o sistema responde 400 com a mensagem "A foto deve ter no máximo 2 MB." e a foto atual não muda

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
