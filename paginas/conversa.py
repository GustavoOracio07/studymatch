import time

import streamlit as st

from studymatch import sessao, visual
from studymatch.api import ErroAPI

INTERVALO = 8  # segundos; duas telas abertas gastam 5 das 10 requisições que o plano free aceita a cada 20 s
MAX_CARACTERES = 500

api = sessao.api()

if st.button("Voltar para Meus matches", icon=":material/arrow_back:"):
    st.switch_page("paginas/matches.py")

colega = st.session_state.get("conversa")
if not colega:
    st.info("Escolha um colega em Meus matches, na aba Confirmados, para conversar.")
    st.stop()

with visual.hero():
    st.title(f"Conversa com {colega['nome']}")

try:
    aluno = sessao.aluno_atual()
except ErroAPI as e:
    sessao.mostrar_erro(e)
    st.stop()

# Estado desta conversa. `ultima` é o último id que veio da busca: a mensagem enviada entra na tela na hora,
# mas não avança a busca, para não pular uma mensagem do colega com id menor.
estado = sessao.dados_da_sessao("mensagens", dict).setdefault(
    colega["interesse_id"], {"itens": {}, "ultima": None, "buscou_em": None, "enviou": False})

texto = st.chat_input("Escreva uma mensagem", max_chars=MAX_CARACTERES)
if texto:
    try:
        enviada = api.enviar_mensagem(colega["interesse_id"], texto)
    except ErroAPI as e:
        sessao.mostrar_erro(e)
    else:
        estado["itens"][enviada["id"]] = enviada
        estado["enviou"] = True


def buscar():
    """Busca as mensagens novas. Logo depois de um envio, só se a última busca já passou do intervalo."""
    enviou, estado["enviou"] = estado["enviou"], False
    agora = time.monotonic()
    if enviou and estado["buscou_em"] is not None and agora - estado["buscou_em"] < INTERVALO:
        return
    estado["buscou_em"] = agora
    for m in api.mensagens(colega["interesse_id"], estado["ultima"]):
        estado["itens"][m["id"]] = m
        estado["ultima"] = m["id"]


@st.fragment(run_every=INTERVALO)
def conversa():
    try:
        buscar()
    except ErroAPI as e:
        if e.status == 429:
            st.caption("Atualizando a conversa...")
        elif e.status == 401:
            sessao.mostrar_erro(e)
        else:
            st.warning(e.mensagem)

    with st.container(height=420, key="mensagens_conversa", autoscroll=True):
        if not estado["itens"]:
            st.caption("Nenhuma mensagem ainda.")
        for _, m in sorted(estado["itens"].items()):
            minha = m["remetente_id"] == aluno["id"]
            autor = "Você" if minha else colega["nome"]
            with st.chat_message(autor, avatar=":material/person:" if minha else ":material/school:"):
                visual.html_(f'<div class="sm-conversa-autor">{visual.esc(autor)}</div>')
                st.text(m["texto"])  # texto literal: não interpreta HTML nem Markdown


conversa()
