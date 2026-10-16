# Tasks

## 1. Backend (Xano)

- [x] 1.1 Nenhuma alteração no Xano; verificar com `xano workspace push --dry-run` que não há mudanças pendentes

## 2. Frontend (Streamlit) e deploy

- [x] 2.1 Converter `requirements.txt` para UTF-8 e verificar com `file requirements.txt` e `pip install --dry-run -r requirements.txt`
- [x] 2.2 Criar `.python-version` e `render.yaml`; verificar que o YAML é válido e que o comando de start do Blueprint sobe o app localmente com `PORT` definido (`/_stcore/health` responde `ok`)
- [x] 2.3 Reescrever o `README.md` com execução local, testes e passo a passo do Render; verificar que os comandos documentados funcionam como escritos
