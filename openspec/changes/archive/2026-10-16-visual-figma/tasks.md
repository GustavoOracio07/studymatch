# Tasks

## 1. Backend (Xano)

- [x] 1.1 Nenhuma alteração no Xano; verificar com `git diff main --stat -- xano` que nada mudou

## 2. Frontend (Streamlit)

- [x] 2.1 Criar o tema (`.streamlit/config.toml`), o CSS (`assets/`) e `studymatch/visual.py`; verificar com screenshots no Chrome (headless)
- [x] 2.2 Refazer Entrar e Criar conta (3 etapas) no layout do Figma; verificar com `tests/frontend/teste_telas_base.py`
- [x] 2.3 Levar a busca para o Início com cartões, filtros, "Ver perfil" e painel "Seu perfil"; verificar com `tests/frontend/teste_telas_busca.py`
- [x] 2.4 Restilizar Meus matches e Meu perfil e trocar os textos em inglês; verificar com `tests/frontend/teste_telas_matches.py` e `tests/frontend/teste_telas_perfil.py`
- [x] 2.5 Centralizar a logo e o cartão no painel claro das telas de acesso e levar a faixa lilás do topo até a borda direita; verificar com screenshots no Chrome (headless)
- [x] 2.6 Criar a alternância de modo claro/escuro (`assets/estilo_escuro.css`, `assets/estilo_acesso_escuro.css`) com a escolha guardada na sessão; verificar com `tests/frontend/teste_telas_tema.py` e screenshots das telas no modo escuro
