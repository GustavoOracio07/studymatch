import streamlit as st

from studymatch import sessao
from studymatch.api import ErroAPI, XanoAPI, listar_cursos

st.title("Criar conta")

try:
    cursos = listar_cursos()
except ErroAPI as e:
    sessao.mostrar_erro(e)
    st.stop()

id_por_curso = {c["nome"]: c["id"] for c in cursos}

with st.form("cadastro"):
    col1, col2 = st.columns(2)
    nome = col1.text_input("Nome *")
    sobrenome = col2.text_input("Sobrenome *")
    email = st.text_input("E-mail *")
    senha = st.text_input("Senha *", type="password", help="Mínimo de 8 caracteres, com letras e números.")
    telefone = st.text_input("Telefone *", help="Só aparece para quem tiver um match confirmado com você.")
    col3, col4 = st.columns([3, 1])
    curso = col3.selectbox("Curso *", options=list(id_por_curso), index=None, placeholder="Escolha o seu curso")
    semestre = col4.number_input("Semestre *", min_value=1, max_value=12, value=1, step=1)
    sobre_mim = st.text_area("Sobre mim", placeholder="Conte um pouco sobre você e como gosta de estudar.")
    enviado = st.form_submit_button("Criar conta", type="primary")

if enviado:
    obrigatorios = [nome, sobrenome, email, senha, telefone]
    if any(not campo.strip() for campo in obrigatorios) or curso is None:
        st.error("Preencha todos os campos marcados com *.")
    else:
        dados = {
            "name": nome.strip(),
            "sobrenome": sobrenome.strip(),
            "email": email.strip(),
            "password": senha,
            "telefone": telefone.strip(),
            "curso_id": id_por_curso[curso],
            "semestre": int(semestre),
            "sobre_mim": sobre_mim.strip(),
        }
        try:
            resposta = XanoAPI().cadastrar(dados)
            sessao.entrar(resposta["authToken"])
        except ErroAPI as e:
            sessao.mostrar_erro(e)
        else:
            st.rerun()

st.page_link("paginas/entrar.py", label="Já tem conta? Entre", icon=":material/login:")
