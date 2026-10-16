# StudyMatch

Aplicação web que conecta alunos com dificuldades acadêmicas em comum para estudarem juntos. O aluno informa as disciplinas em que tem dificuldade e os horários livres, e o sistema sugere colegas compatíveis. A compatibilidade é calculada assim: 60% pelas disciplinas em comum e 40% pelos horários em comum. Quando os dois demonstram interesse, o match é confirmado e o telefone do colega é liberado.

Projeto Integrador — Innovation Lab: Advanced No/Low Code — ADS, Faculdade Impacta, 2026.2.

- **Backend:** [Xano](https://www.xano.com/) (banco, API REST e autenticação). O código XanoScript fica em [`xano/`](xano/).
- **Frontend:** [Streamlit](https://streamlit.io/), que só consome a API do Xano.
- **Especificação:** [OpenSpec](openspec/). As specs consolidadas ficam em `openspec/specs/` e o histórico de changes em `openspec/changes/archive/`.
- **Contexto do projeto:** [`docs/project-overview.md`](docs/project-overview.md), [`docs/domain-model.md`](docs/domain-model.md) e [`AGENTS.md`](AGENTS.md).

## Estrutura

```text
app.py                 ponto de entrada (navegação conforme o login)
paginas/               telas: entrar, cadastro, início, perfil, buscar, matches, sair
studymatch/            cliente da API do Xano (api.py), sessão (sessao.py) e rótulos (dominio.py)
tests/api/             testes de API contra o Xano
tests/frontend/        testes do cliente (offline) e das telas (AppTest)
xano/                  workspace do Xano em XanoScript (sincronizado com o Xano CLI)
render.yaml            Blueprint de deploy no Render
```

## Rodar localmente

Pré-requisito: Python 3.14 (a mesma versão de `.python-version`).

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    |    Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

Configure a URL da API do Xano: copie `.streamlit/secrets.toml.example` para `.streamlit/secrets.toml` e preencha `XANO_API_URL`. Ela é a URL base do grupo de API **Authentication**, no formato `https://<instancia>.xano.io/api:<canonical>`. O `secrets.toml` é ignorado pelo Git. Em vez dele, também dá para usar a variável de ambiente `XANO_API_URL`, que tem prioridade.

```bash
streamlit run app.py
```

O app abre em http://localhost:8501.

## Testes

Os testes de API e de tela rodam contra o Xano de verdade: criam alunos de teste (`teste.*@studymatch.test`) e apagam todos no final. O plano free do Xano aceita 10 requisições a cada 20 s, por isso os testes esperam entre as chamadas e levam alguns minutos.

```bash
python tests/frontend/teste_api_cliente.py   # cliente da API, offline e rápido
python tests/api/teste_seguranca.py          # autenticação e controle de acesso
python tests/api/teste_perfil.py             # perfil, disciplinas e disponibilidade
python tests/api/teste_busca.py              # compatibilidade e interesse
python tests/api/teste_matches.py            # meus matches e telefone após o match
python tests/frontend/teste_telas_base.py    # login, cadastro e logout
python tests/frontend/teste_telas_perfil.py
python tests/frontend/teste_telas_busca.py
python tests/frontend/teste_telas_matches.py
```

Por padrão, os testes usam a API do projeto. Para apontar para outra, defina `XANO_API_URL`.

## Backend (Xano)

As alterações no backend são feitas nos arquivos `.xs` em `xano/` e publicadas com o [Xano CLI](https://docs.xano.com/):

```bash
cd xano
xano workspace push --dry-run   # revise a prévia
xano workspace push             # publica só os arquivos alterados
```

Depois do push, rode `xano workspace pull` em uma pasta temporária e copie o resultado para `xano/`. Assim o formato local fica idêntico ao do servidor.

## Deploy no Render

O repositório já tem o Blueprint [`render.yaml`](render.yaml): um web service Python no plano free, que instala `requirements.txt`, sobe o Streamlit em `0.0.0.0:$PORT` e usa `/_stcore/health` como health check. A versão do Python vem de `.python-version`.

1. Entre no [Render](https://dashboard.render.com/) e conecte a sua conta do GitHub.
2. Clique em **New → Blueprint** e escolha o repositório `studymatch` (branch `main`).
3. O Render lê o `render.yaml` e pede o valor de **`XANO_API_URL`**. Informe a URL base da API (a mesma do `secrets.toml`).
4. Clique em **Apply**. O primeiro build leva alguns minutos. Quando terminar, o app fica em `https://studymatch-xxxx.onrender.com`.
5. A cada commit na `main`, o Render faz um novo deploy automaticamente (`autoDeployTrigger: commit`).

Observações:
- No plano free, o serviço "dorme" depois de um tempo sem acesso. O primeiro acesso seguinte demora cerca de um minuto.
- Para trocar a URL da API depois, vá em **Environment** no painel do serviço e altere `XANO_API_URL`.
- Sem o Blueprint, dá para criar um **Web Service** manualmente com os mesmos comandos: build `pip install -r requirements.txt` e start `streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`.
