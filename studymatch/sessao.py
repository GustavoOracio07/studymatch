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
    tema_escuro = st.session_state.get("tema_escuro")  # preferência visual sobrevive ao logout
    st.session_state.clear()
    if tema_escuro:
        st.session_state["tema_escuro"] = tema_escuro
    if aviso:
        st.session_state["aviso"] = aviso


def aluno_atual():
    """Dados do aluno logado (`GET /auth/me`), guardados na sessão para poupar requisições."""
    return dados_da_sessao("aluno", lambda: api().eu())


def recarregar_aluno():
    st.session_state.pop("aluno", None)
    return aluno_atual()


def dados_da_sessao(chave, carregar):
    """Guarda na sessão o resultado de `carregar()` para não repetir a chamada a cada interação."""
    if chave not in st.session_state:
        st.session_state[chave] = carregar()
    return st.session_state[chave]


def invalidar(*chaves):
    for chave in chaves:
        st.session_state.pop(chave, None)


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
