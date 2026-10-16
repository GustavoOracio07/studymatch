import streamlit as st

from studymatch import sessao

sessao.sair(aviso="Você saiu da sua conta.")
st.rerun()
