# Design

## Armazenamento

- Campo `image? Foto?` na tabela `user`. O Xano guarda os metadados (`path`, `name`, `size`, `mime`, `meta.width/height`); o arquivo fica no armazenamento de arquivos do Xano.
- Upload com `storage.create_image` e `access = "public"`. A URL pública é montada no backend a partir do `path` e devolvida como `foto_url`, para o Streamlit não precisar conhecer o formato de URL do Xano.
- Por que pública e não privada: com `access = "private"` cada listagem teria que gerar uma URL assinada por colega (`storage.sign_private_url`), o que aumenta o custo de cada chamada no plano free (10 requisições a cada 20 s). A foto não é dado sensível no StudyMatch: fica visível para os colegas compatíveis, assim como o nome. O telefone continua sendo liberado só após o match.

## Endpoints

- `POST /auth/me/foto`, `auth = "user"`, input `file? foto`.
  1. `precondition` de que o arquivo foi enviado.
  2. Validar o tamanho (até 2 MB) e o tipo (JPEG, PNG ou WEBP). `storage.create_image` já recusa extensões que não são imagem, mas com erro 500; a validação explícita devolve `inputerror` com mensagem em português.
  3. `storage.create_image` → `db.edit user` com `Foto`.
  4. Se havia foto anterior, `storage.delete_file` do `path` antigo (depois de gravar a nova, para não deixar o aluno sem foto se o upload falhar).
  5. Resposta: o mesmo perfil de `GET /auth/me`, com `foto_url`.
- `DELETE /auth/me/foto`, `auth = "user"`: limpa `Foto` e apaga o arquivo. Sem foto, responde 200 sem erro (idempotente).
- O dono é sempre `$auth.id`; não há `user_id` no input, então um aluno não consegue trocar a foto de outro.

## Saída de `foto_url`

- `GET/PATCH /auth/me`: incluir `Foto` no `output` e acrescentar `foto_url`.
- `GET /compativeis` e `GET /meus_matches`: incluir `Foto` no `output` do colega e devolver `foto_url` no item. O objeto `Foto` bruto não é devolvido.
- Para evitar repetir a montagem da URL, criar a função `StudyMatch/url_foto` (input `Foto`, retorna texto ou `null`).

## Frontend

- `api.py`: `enviar_foto(arquivo)` faz `POST` multipart; `remover_foto()` faz `DELETE`. O `_req` atual envia JSON; o upload passa `files=` em vez de `json=`.
- `visual.py`: função `avatar(foto_url, nome, sobrenome)` que mostra a imagem redonda ou, sem foto, um círculo com as iniciais, respeitando o modo claro/escuro.
- `perfil.py`, aba "Dados": avatar atual, `st.file_uploader` (tipos jpg, jpeg, png, webp) com botão "Salvar foto" e botão "Remover foto". A foto fica fora do `st.form` dos dados, para não depender do botão "Salvar dados".
- `inicio.py` e `matches.py`: usar `avatar` nos cards dos colegas.
- O Streamlit valida tipo e tamanho só para dar retorno rápido; a regra vale no Xano.

## Riscos

- A sintaxe exata de validação de tamanho/tipo do arquivo no input precisa ser conferida no Xano Developer MCP antes do apply.
- O plano free do Xano tem limite de armazenamento; se ele acabar, o upload falha e o app mostra o erro da API.
