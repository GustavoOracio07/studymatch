"""Identidade visual do StudyMatch: CSS e pedaços de HTML usados pelas telas.

Só apresentação. Todo texto vindo de usuários passa por `esc()` antes de ir para o HTML.
"""
import html
import pathlib

import streamlit as st

ASSETS = pathlib.Path(__file__).resolve().parents[1] / "assets"
LOGO = str(ASSETS / "logo.svg")
LOGO_ICONE = str(ASSETS / "logo_icone.svg")

_ICONES = {
    "usuario": '<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    "cadeado": '<rect width="18" height="11" x="3" y="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    "livro": '<path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/>',
    "relogio": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "curso": '<path d="M22 10 12 5 2 10l10 5 10-5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/>',
    "telefone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2'
                ' 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3'
                'a2 2 0 0 1 2.1-.4c.9.3 1.9.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
    "mensagem": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    "check": '<polyline points="20 6 9 17 4 12"/>',
    "seta": '<polyline points="9 18 15 12 9 6"/>',
    "coracao": '<path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2'
               'A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7z"/>',
}

_CORES_AVATAR = ["#5B3FE4", "#0E7490", "#B45309", "#BE185D", "#15803D", "#1D4ED8", "#7C3AED", "#C2410C"]


def esc(texto):
    return html.escape(str(texto or ""))


def html_(conteudo, onde=st):
    """Mostra um pedaço de HTML (sem espaço extra) no container `onde`."""
    onde.markdown(conteudo, unsafe_allow_html=True)


def aplicar_estilo():
    st.html(ASSETS / "estilo.css")


def aplicar_estilo_acesso():
    st.html(ASSETS / "estilo_acesso.css")


def icone(nome, tamanho=15):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{tamanho}" height="{tamanho}" viewBox="0 0 24 24" '
            f'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            f'{_ICONES[nome]}</svg>')


def iniciais(nome, sobrenome=""):
    letras = [p[0] for p in f"{nome or ''} {sobrenome or ''}".split() if p]
    return esc("".join(letras[:1] + letras[-1:]).upper() if len(letras) > 1 else "".join(letras).upper() or "?")


def avatar(nome, sobrenome, semente, grande=False):
    cor = _CORES_AVATAR[(semente or 0) % len(_CORES_AVATAR)]
    classe = "sm-avatar sm-avatar-grande" if grande else "sm-avatar"
    return f'<div class="{classe}" style="background:{cor}">{iniciais(nome, sobrenome)}</div>'


def selo(percentual):
    percentual = percentual or 0
    cor = "verde" if percentual >= 85 else "amarelo" if percentual >= 70 else "laranja"
    return f'<span class="sm-selo sm-selo-{cor}">{percentual}% de compatibilidade</span>'


def sigla_curso(nome_curso):
    """'Análise e Desenvolvimento de Sistemas' -> 'ADS'."""
    palavras = [p for p in (nome_curso or "").split() if len(p) > 2]
    return "".join(p[0].upper() for p in palavras) or esc(nome_curso)


def linha(nome_icone, texto, classe=""):
    return f'<div class="sm-linha {classe}">{icone(nome_icone, 14)}<span>{texto}</span></div>'


def hero():
    """Faixa lilás do topo das páginas, como no Figma."""
    return st.container(key="hero")


# --- Telas de acesso ---------------------------------------------------------

_PAINEL = """
<div class="sm-painel">
  <div class="sm-impacta"><span class="sm-impacta-fac">Faculdade</span><span class="sm-impacta-nome">IMPACTA</span></div>
  <div class="sm-bv">
    <p class="sm-bv-1">Bem-vindo ao</p>
    <p class="sm-bv-2">StudyMatch</p>
    <p class="sm-tagline">Seu próximo parceiro de estudos pode estar a um <b>MATCH</b> de distância</p>
  </div>
  <p class="sm-rodape">Encontre colegas com as mesmas dificuldades e horários livres para estudar junto.</p>
</div>
"""

_LOGO_CIRCULO = """
<div class="sm-logo-circulo">
  <svg width="54" height="54" viewBox="0 0 54 54" xmlns="http://www.w3.org/2000/svg">
    <circle cx="27" cy="27" r="27" fill="#1E1F22"/>
    <path d="M16 36 L26 17 L31 17 L21 36 Z" fill="#1A73E8"/>
    <path d="M27 29 L31 22 L38 36 L31 36 Z" fill="#1A73E8"/>
  </svg>
</div>
"""


def layout_acesso():
    """Monta o painel escuro e devolve o cartão branco onde vai o formulário."""
    aplicar_estilo_acesso()
    esquerda, direita = st.columns([0.43, 0.57], gap=0)
    html_(_PAINEL, esquerda)
    lado = direita.container(key="lado_form")
    html_(_LOGO_CIRCULO, lado)
    return lado.container(key="cartao_acesso")


def etapas(atual, total=3):
    partes = []
    for n in range(1, total + 1):
        if n < atual:
            partes.append(f'<div class="sm-etapa sm-etapa-feita">{icone("check", 14)}</div>')
        elif n == atual:
            partes.append(f'<div class="sm-etapa sm-etapa-atual">{n}</div>')
        else:
            partes.append(f'<div class="sm-etapa">{n}</div>')
        if n < total:
            classe = "sm-traco sm-traco-feito" if n < atual else "sm-traco"
            partes.append(f'<div class="{classe}"></div>')
    return f'<div class="sm-etapas">{"".join(partes)}</div>'


def titulo_acesso(nome_icone, titulo, subtitulo=""):
    sub = f'<p class="sm-acesso-sub">{subtitulo}</p>' if subtitulo else ""
    return f'<div class="sm-acesso-titulo">{icone(nome_icone, 18)}<span>{titulo}</span></div>{sub}'
