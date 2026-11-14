# Tasks

## 1. Backend (Xano)

- [x] 1.1 Adicionar `text? Foto_dados?` à tabela `user`
- [x] 1.2 `StudyMatch/url_foto`: devolver `Foto_dados` quando houver; senão, a URL do arquivo antigo
- [x] 1.3 `POST /auth/me/foto`: receber a data URL, validar começo e tamanho, gravar em `Foto_dados`, limpar `Foto` e apagar o arquivo antigo
- [x] 1.4 `DELETE /auth/me/foto`: limpar `Foto` e `Foto_dados`
- [x] 1.5 Passar `Foto_dados` para `url_foto` em `GET`/`PATCH /auth/me`, `GET /compativeis` e `GET /meus_matches`, sem devolver o campo
- [x] 1.6 `xano workspace push --dry-run` e publicar
- [x] 1.7 Ajustar e rodar `tests/api/teste_foto.py`

## 2. Frontend (Streamlit)

- [x] 2.1 `api.py`: `foto_data_url()` (256x256, JPEG) e `enviar_foto(conteudo)` em JSON; cobrir em `teste_api_cliente.py`
- [x] 2.2 `perfil.py`: usar o novo `enviar_foto`
- [x] 2.3 Rodar `tests/frontend/teste_telas_perfil.py`
