"""Ponto de entrada do StudyMatch: define as páginas visíveis conforme o login."""
import streamlit as st

from studymatch import sessao

st.set_page_config(page_title="StudyMatch", page_icon=":material/school:", layout="centered")

if sessao.esta_logado():
    paginas = [
        st.Page("paginas/inicio.py", title="Início", icon=":material/home:", default=True),
        st.Page("paginas/perfil.py", title="Meu perfil", icon=":material/person:"),
        st.Page("paginas/sair.py", title="Sair", icon=":material/logout:"),
    ]
else:
    paginas = [
        st.Page("paginas/entrar.py", title="Entrar", icon=":material/login:", default=True),
        st.Page("paginas/cadastro.py", title="Criar conta", icon=":material/person_add:"),
    ]

st.navigation(paginas).run()
