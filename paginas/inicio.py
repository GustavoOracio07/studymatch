import streamlit as st

from studymatch import sessao
from studymatch.api import ErroAPI

try:
    aluno = sessao.aluno_atual()
except ErroAPI as e:
    sessao.mostrar_erro(e)
    st.stop()

st.title(f"Olá, {aluno['Name']}!")
st.write(
    "O StudyMatch sugere colegas que têm dificuldade nas mesmas disciplinas que você "
    "e horários livres em comum."
)
