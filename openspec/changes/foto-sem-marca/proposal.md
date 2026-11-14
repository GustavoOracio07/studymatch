# Foto de perfil sem marca d'água

## Por quê
No plano free do Xano, toda imagem gravada com `storage.create_image` recebe a marca "Powered by Xano" no canto inferior esquerdo. As fotos de perfil apareciam com essa marca.

## O que muda
- O frontend reduz a foto para 256x256 (corte central) em JPEG e envia como data URL no campo `foto` (JSON) de `POST /auth/me/foto`.
- O Xano grava a data URL no novo campo `user.Foto_dados` (texto), sem usar o armazenamento de imagens.
- O Xano valida o começo da data URL (`data:image/jpeg;base64,`) e o tamanho (até 300 mil caracteres).
- `foto_url` passa a ser a data URL. Fotos antigas (campo `Foto`) continuam aparecendo até o aluno enviar outra; ao enviar ou remover, o arquivo antigo é apagado.

## Impacto
- Xano: tabela `user`, `StudyMatch/url_foto`, `POST`/`DELETE /auth/me/foto`, `GET`/`PATCH /auth/me`, `GET /compativeis`, `GET /meus_matches`.
- Streamlit: `studymatch/api.py` (`foto_data_url`, `enviar_foto`) e `paginas/perfil.py`.
- Testes: `tests/api/teste_foto.py`, `tests/frontend/teste_api_cliente.py`, `tests/frontend/teste_telas_perfil.py`.
