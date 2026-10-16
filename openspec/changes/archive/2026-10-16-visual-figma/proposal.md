# Proposal

## Why

O grupo tem um protótipo no Figma (telas de acesso com cadastro em 3 etapas, Início com colegas compatíveis e resumo do perfil, e Meus matches). Hoje o frontend usa o visual padrão do Streamlit e mostra alguns textos em inglês (como "Select all" e "Press Enter to submit form").

## What Changes

- Tema do Streamlit (`.streamlit/config.toml`) com as cores e a fonte Inter do Figma, mais CSS próprio em `assets/` e helpers de HTML em `studymatch/visual.py`.
- Telas de acesso: painel escuro "Bem-vindo ao StudyMatch" à esquerda e cartão branco à direita. O cadastro passa a ter 3 etapas (nome → senha e e-mail → curso, semestre, telefone e sobre mim). A API só é chamada na última etapa.
- Menu lateral igual ao do Figma: Início, Meus matches, Meu perfil (e Sair). **A busca de colegas passa a ser o conteúdo do Início**, com cartões (avatar com iniciais, selo de compatibilidade, disciplinas, horários e sobre mim), filtros por matéria e semestre, ordenação, diálogo "Ver perfil" e o painel "Seu perfil" com o percentual de perfil completo.
- Meus matches e Meu perfil no mesmo estilo, com faixa no topo e cartões.
- Botão "Modo escuro"/"Modo claro" no menu lateral (e no canto das telas de acesso). O modo claro segue as cores do Figma; o escuro usa fundo escuro com roxo `#5B3FE4` nos destaques. A escolha fica na sessão, vale em todas as páginas e continua após sair.
- Textos em inglês do Streamlit removidos ou trocados ("Select all", "Press Enter to submit form", "Running...", placeholders).

**Fora do escopo:**
- Qualquer mudança no Xano, nos endpoints ou nas regras de negócio.
- Campos do Figma que não existem no backend: "Formato" (presencial/online), "Email Impacta", foto de perfil, data do match e matérias/disponibilidade no cadastro.

## Capabilities

### New Capabilities
<!-- Nenhuma. -->

### Modified Capabilities
- `interface-web`: menu com Início, Meus matches e Meu perfil; cadastro em 3 etapas; alternância de modo claro/escuro.
- `busca-compatibilidade`: a lista de colegas compatíveis passa a ficar na página Início.

## Impact

- Frontend apenas: `app.py`, `paginas/`, `studymatch/visual.py`, `assets/`, `.streamlit/config.toml` e os testes de tela. `paginas/buscar.py` foi removida (o conteúdo foi para `paginas/inicio.py`).
