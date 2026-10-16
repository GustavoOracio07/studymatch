import streamlit as st

from studymatch import sessao, visual
from studymatch.api import ErroAPI, XanoAPI

with visual.layout_acesso():
    sessao.mostrar_aviso()
    visual.html_(visual.titulo_acesso("usuario", "Entre na sua conta", "Use o e-mail e a senha do seu cadastro"))

    with st.form("entrar", border=False):
        email = st.text_input("E-mail", placeholder="Endereço de e-mail", label_visibility="collapsed")
        senha = st.text_input("Senha", type="password", placeholder="Senha", label_visibility="collapsed")
        with st.container(horizontal=True, horizontal_alignment="distribute", vertical_alignment="center"):
            criar_conta = st.form_submit_button("Criar conta", type="tertiary")
            enviado = st.form_submit_button("Entrar", type="primary")

    if criar_conta:
        st.switch_page("paginas/cadastro.py")

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
