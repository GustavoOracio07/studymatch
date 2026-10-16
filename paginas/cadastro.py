"""Cadastro em 3 etapas (como no Figma). Os dados ficam na sessão e vão para a API só na última etapa."""
import streamlit as st

from studymatch import sessao, visual
from studymatch.api import ErroAPI, XanoAPI, listar_cursos

PASSO, DADOS = "cadastro_passo", "cadastro_dados"
SEMESTRES = {f"{n}º semestre": n for n in range(1, 13)}

passo = st.session_state.setdefault(PASSO, 1)
dados = st.session_state.setdefault(DADOS, {})


def ir_para(novo_passo, **valores):
    dados.update(valores)
    st.session_state[PASSO] = novo_passo
    st.rerun()


def botoes(voltar, avancar):
    with st.container(horizontal=True, horizontal_alignment="distribute", vertical_alignment="center"):
        clicou_voltar = st.form_submit_button(voltar, type="tertiary",
                                              icon=":material/arrow_back:" if voltar == "Voltar" else None)
        clicou_avancar = st.form_submit_button(avancar, type="primary")
    return clicou_voltar, clicou_avancar


with visual.layout_acesso():
    visual.html_(visual.etapas(passo))

    if passo == 1:
        visual.html_(visual.titulo_acesso("usuario", "Como você se chama?",
                                          "Informe seu nome completo para criar sua conta"))
        with st.form("cadastro_1", border=False):
            nome = st.text_input("Nome *", value=dados.get("name", ""), placeholder="Nome",
                                 label_visibility="collapsed")
            sobrenome = st.text_input("Sobrenome *", value=dados.get("sobrenome", ""), placeholder="Sobrenome",
                                      label_visibility="collapsed")
            entrar, avancar = botoes("Entrar", "Avançar")
        if entrar:
            st.switch_page("paginas/entrar.py")
        if avancar:
            if not nome.strip() or not sobrenome.strip():
                st.error("Preencha o nome e o sobrenome.")
            else:
                ir_para(2, name=nome.strip(), sobrenome=sobrenome.strip())

    elif passo == 2:
        visual.html_(visual.titulo_acesso("cadeado", "Insira seu e-mail e crie uma senha segura"))
        with st.form("cadastro_2", border=False):
            senha = st.text_input("Senha *", type="password", value=dados.get("password", ""), placeholder="Senha",
                                  label_visibility="collapsed", help="Mínimo de 8 caracteres, com letras e números.")
            confirmar = st.text_input("Confirmar senha *", type="password", value=dados.get("password", ""),
                                      placeholder="Confirmar senha", label_visibility="collapsed")
            email = st.text_input("E-mail *", value=dados.get("email", ""), placeholder="Endereço de e-mail",
                                  label_visibility="collapsed")
            voltar, avancar = botoes("Voltar", "Avançar")
        if voltar:
            ir_para(1)
        if avancar:
            if not senha or not confirmar or not email.strip():
                st.error("Preencha a senha, a confirmação e o e-mail.")
            elif senha != confirmar:
                st.error("As senhas não conferem.")
            else:
                ir_para(3, password=senha, email=email.strip())

    else:
        try:
            cursos = listar_cursos()
        except ErroAPI as e:
            sessao.mostrar_erro(e)
            st.stop()
        id_por_curso = {c["nome"]: c["id"] for c in cursos}

        visual.html_(visual.titulo_acesso("usuario", "Conte mais sobre você"))
        with st.form("cadastro_3", border=False):
            curso = st.selectbox("Curso *", options=list(id_por_curso), index=None, placeholder="Curso *",
                                 label_visibility="collapsed")
            semestre = st.selectbox("Semestre *", options=list(SEMESTRES), index=None, placeholder="Semestre *",
                                    label_visibility="collapsed")
            telefone = st.text_input("Telefone *", placeholder="Telefone *", label_visibility="collapsed",
                                     help="Só aparece para quem tiver um match confirmado com você.")
            sobre_mim = st.text_area("Sobre mim", placeholder="Sobre mim (opcional)", label_visibility="collapsed",
                                     height=90)
            voltar, criar = botoes("Voltar", "Criar conta")
        if voltar:
            ir_para(2)
        if criar:
            if curso is None or semestre is None or not telefone.strip():
                st.error("Preencha curso, semestre e telefone.")
            else:
                try:
                    resposta = XanoAPI().cadastrar({
                        **dados,
                        "telefone": telefone.strip(),
                        "curso_id": id_por_curso[curso],
                        "semestre": SEMESTRES[semestre],
                        "sobre_mim": sobre_mim.strip(),
                    })
                    sessao.entrar(resposta["authToken"])
                except ErroAPI as e:
                    sessao.mostrar_erro(e)
                else:
                    st.session_state.pop(PASSO, None)
                    st.session_state.pop(DADOS, None)
                    st.rerun()
