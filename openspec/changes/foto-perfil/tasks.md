# Tasks

## 1. Backend (Xano)

- [ ] 1.1 Conferir no Xano Developer MCP a sintaxe de `file?` input, `storage.create_image`, `storage.delete_file` e da validação de tamanho/tipo
- [ ] 1.2 Adicionar `image? Foto?` à tabela `user`
- [ ] 1.3 Criar a função `StudyMatch/url_foto` (monta a URL pública a partir do `path`, ou `null`)
- [ ] 1.4 Criar `POST /auth/me/foto` (validação de tipo e de 2 MB, grava a nova foto, apaga a anterior, devolve o perfil com `foto_url`)
- [ ] 1.5 Criar `DELETE /auth/me/foto` (limpa o campo e apaga o arquivo; idempotente)
- [ ] 1.6 Incluir `foto_url` em `GET /auth/me`, `PATCH /auth/me`, `GET /compativeis` e `GET /meus_matches`, sem devolver o objeto `Foto`
- [ ] 1.7 Apagar o arquivo da foto em `StudyMatch/excluir_usuario`
- [ ] 1.8 Revisar com `git diff`, rodar `xano workspace push --dry-run`, publicar e alinhar com `xano workspace pull`
- [ ] 1.9 Criar `tests/api/teste_foto.py` cobrindo os cenários de `perfil-aluno` (envio, troca, PDF, 3 MB, sem arquivo, remoção, sem token) e a foto apagada junto com a conta
- [ ] 1.10 Rodar `teste_busca.py`, `teste_matches.py` e `teste_seguranca.py` e verificar `foto_url` nas listagens

## 2. Frontend (Streamlit)

- [ ] 2.1 `api.py`: `enviar_foto(arquivo)` (multipart) e `remover_foto()`; cobrir em `tests/frontend/teste_api_cliente.py`
- [ ] 2.2 `visual.py`: `avatar(foto_url, nome, sobrenome)` com foto redonda ou iniciais, nos modos claro e escuro
- [ ] 2.3 `perfil.py`: avatar, seletor de arquivo, "Salvar foto" e "Remover foto" na aba "Dados"; atualizar `st.session_state["aluno"]` e invalidar `compativeis`
- [ ] 2.4 `inicio.py` e `matches.py`: avatar nos cards dos colegas
- [ ] 2.5 Ajustar `tests/frontend/teste_telas_perfil.py` e verificar no navegador o fluxo de envio, troca e remoção da foto
