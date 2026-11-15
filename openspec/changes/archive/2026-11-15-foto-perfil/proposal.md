# Proposal

## Why

Hoje os colegas compatíveis e os matches aparecem só com nome, semestre e "sobre mim". Uma foto de perfil ajuda o aluno a reconhecer o colega na faculdade e deixa a busca mais pessoal, sem mudar a regra de compatibilidade.

## What Changes

- A tabela `user` ganha o campo opcional `Foto` (tipo `image`).
- Novo endpoint `POST /auth/me/foto` (multipart, campo `foto`): o aluno envia uma imagem JPEG, PNG ou WEBP de até 2 MB. O Xano guarda a imagem, pede a exclusão da foto anterior e devolve o perfil.
- Novo endpoint `DELETE /auth/me/foto`: remove a foto do perfil do aluno e pede a exclusão do arquivo.
- `GET /auth/me`, `PATCH /auth/me`, `GET /compativeis` e `GET /meus_matches` passam a devolver `foto_url` (URL pública da imagem, ou `null` sem foto).
- `StudyMatch/excluir_usuario` pede também a exclusão do arquivo da foto ao excluir a conta.
- Streamlit: na aba "Dados" do Meu perfil, o aluno vê a foto atual, envia uma nova ou remove. Os cards de colegas no Início e em Meus matches mostram a foto; sem foto, mostram um avatar com as iniciais.

**Fora do escopo:**
- Foto no cadastro (a foto é opcional e é adicionada depois, no perfil).
- Recorte, redimensionamento ou edição da imagem.
- Moderação de conteúdo das fotos.
- Mais de uma foto por aluno.
- Esconder a foto até o match: a foto é visível para os colegas compatíveis, como o nome.
- Garantir que o arquivo some do armazenamento: no plano free, `storage.delete_file` não dá erro, mas o arquivo continua acessível pelo link antigo (ver design).

## Capabilities

### New Capabilities
<!-- Nenhuma. -->

### Modified Capabilities
- `perfil-aluno`: foto de perfil (envio, troca, remoção e validação) e exibição na página Meu perfil.
- `busca-compatibilidade`: a lista de compatíveis inclui `foto_url` e o card mostra a foto.
- `meus-matches`: a lista inclui `foto_url` e o card mostra a foto.
- `controle-de-acesso`: a exclusão em cascata do usuário inclui o arquivo da foto.

## Impact

- Xano: `table/user.xs`, novos `api/authentication/auth/me_foto_POST.xs` e `me_foto_DELETE.xs`, `auth/me_GET.xs`, `auth/me_PATCH.xs`, `compativeis_GET.xs`, `meus_matches_GET.xs`, `function/study_match/excluir_usuario.xs`.
- Streamlit: `studymatch/api.py`, `studymatch/visual.py`, `paginas/perfil.py`, `paginas/inicio.py`, `paginas/matches.py`.
- Testes: novo `tests/api/teste_foto.py`; ajustes em `tests/frontend/teste_api_cliente.py` e `tests/frontend/teste_telas_perfil.py`.
- Armazenamento: as fotos ocupam o espaço de arquivos do plano free do Xano; o limite de 2 MB por foto controla o uso.
