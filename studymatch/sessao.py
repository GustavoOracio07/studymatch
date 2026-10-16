"""Estado de login do aluno na sessão do Streamlit."""
import streamlit as st

from studymatch.api import ErroAPI, XanoAPI


def esta_logado():
    return bool(st.session_state.get("token"))


def api():
    """Cliente da API com o token do aluno logado (se houver)."""
    return XanoAPI(st.session_state.get("token"))


def entrar(token):
    st.session_state["token"] = token
    st.session_state["aluno"] = XanoAPI(token).eu()


def sair(aviso=None):
    st.session_state.clear()
    if aviso:
        st.session_state["aviso"] = aviso


def aluno_atual():
    """Dados do aluno logado (`GET /auth/me`), guardados na sessão para poupar requisições."""
    if "aluno" not in st.session_state:
        st.session_state["aluno"] = api().eu()
    return st.session_state["aluno"]


def recarregar_aluno():
    st.session_state.pop("aluno", None)
    return aluno_atual()


def mostrar_erro(erro: ErroAPI):
    """Mostra o erro da API. Se a sessão expirou, desloga e volta para a tela de login."""
    if erro.status == 401 and esta_logado():
        sair(aviso=erro.mensagem)
        st.rerun()
    st.error(erro.mensagem)


def mostrar_aviso():
    aviso = st.session_state.pop("aviso", None)
    if aviso:
        st.warning(aviso)
