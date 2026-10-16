"""Cliente da API do Xano usado por todas as telas.

O frontend só consome a API: as regras de negócio e as validações ficam no Xano.
"""
import os

import requests
import streamlit as st

MSG_LIMITE = "Muitas requisições em pouco tempo. Aguarde alguns segundos e tente de novo."
MSG_REDE = "Não foi possível falar com o servidor. Verifique sua conexão e tente de novo."
MSG_SESSAO_EXPIRADA = "Sua sessão expirou. Entre de novo."
MSG_SEM_CONFIGURACAO = "A variável XANO_API_URL não está configurada. Veja o README."


class ErroAPI(Exception):
    """Erro devolvido pela API (ou de comunicação com ela), com mensagem pronta para a tela."""

    def __init__(self, mensagem, status=None):
        super().__init__(mensagem)
        self.mensagem = mensagem
        self.status = status


def url_base():
    """URL base da API: variável de ambiente (Render) ou `.streamlit/secrets.toml` (local)."""
    url = os.environ.get("XANO_API_URL")
    if not url:
        try:
            url = st.secrets.get("XANO_API_URL")
        except Exception:  # sem secrets.toml
            url = None
    if not url:
        raise ErroAPI(MSG_SEM_CONFIGURACAO)
    return url


class XanoAPI:
    def __init__(self, token=None, base=None, http=None):
        self.token = token
        self.base = (base or url_base()).rstrip("/")
        self._http = http or requests

    def _req(self, metodo, caminho, **kwargs):
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        try:
            r = self._http.request(metodo, self.base + caminho, headers=headers, timeout=20, **kwargs)
        except requests.RequestException as e:
            raise ErroAPI(MSG_REDE) from e

        if r.status_code == 429:
            raise ErroAPI(MSG_LIMITE, 429)
        if r.status_code == 401 and self.token:
            raise ErroAPI(MSG_SESSAO_EXPIRADA, 401)
        if r.status_code >= 400:
            try:
                mensagem = r.json().get("message")
            except ValueError:
                mensagem = None
            raise ErroAPI(mensagem or f"Erro {r.status_code} ao falar com o servidor.", r.status_code)
        if not r.content:
            return None
        return r.json()

    # --- autenticação
    def login(self, email, senha):
        return self._req("POST", "/auth/login", json={"email": email, "password": senha})

    def cadastrar(self, dados):
        return self._req("POST", "/auth/signup", json=dados)

    def eu(self):
        return self._req("GET", "/auth/me")

    # --- catálogo (público)
    def cursos(self):
        return self._req("GET", "/curso")

    def disciplinas(self):
        return self._req("GET", "/disciplina")


@st.cache_data(ttl=600, show_spinner=False)
def listar_cursos():
    """Cursos mudam pouco e são públicos: cache de 10 minutos para poupar o limite de requisições."""
    return XanoAPI().cursos()


@st.cache_data(ttl=600, show_spinner=False)
def listar_disciplinas():
    return XanoAPI().disciplinas()
