import streamlit as st

from studymatch import sessao
from studymatch.api import ErroAPI, XanoAPI

st.title("StudyMatch")
st.caption("Encontre colegas com as mesmas dificuldades e horários para estudar junto.")
sessao.mostrar_aviso()

with st.form("entrar"):
    st.subheader("Entrar")
    email = st.text_input("E-mail")
    senha = st.text_input("Senha", type="password")
    enviado = st.form_submit_button("Entrar", type="primary")

if enviado:
    if not email.strip() or not senha:
        st.error("Preencha o e-mail e a senha.")
    else:
        try:
            resposta = XanoAPI().login(email.strip(), senha)
            sessao.entrar(resposta["authToken"])
        except ErroAPI as e:
            sessao.mostrar_erro(e)
        else:
            st.rerun()

st.page_link("paginas/cadastro.py", label="Ainda não tem conta? Crie a sua", icon=":material/person_add:")
