"""Ponto de entrada do StudyMatch: define as páginas visíveis conforme o login."""
import streamlit as st

from studymatch import sessao, visual

st.set_page_config(page_title="StudyMatch", page_icon=":material/school:", layout="wide")
visual.aplicar_estilo()

if sessao.esta_logado():
    st.logo(visual.LOGO_ESCURO if visual.tema_escuro() else visual.LOGO, icon_image=visual.LOGO_ICONE, size="large")
    visual.botao_tema(st.sidebar)
    paginas = [
        st.Page("paginas/inicio.py", title="Início", icon=":material/home:", default=True),
        st.Page("paginas/matches.py", title="Meus matches", icon=":material/favorite:"),
        st.Page("paginas/perfil.py", title="Meu perfil", icon=":material/person:"),
        st.Page("paginas/sair.py", title="Sair", icon=":material/logout:"),
    ]
    st.navigation(paginas).run()
else:
    paginas = [
        st.Page("paginas/entrar.py", title="Entrar", icon=":material/login:", default=True),
        st.Page("paginas/cadastro.py", title="Criar conta", icon=":material/person_add:"),
    ]
    with st.container(key="tema_acesso"):
        visual.botao_tema()
    st.navigation(paginas, position="hidden").run()
