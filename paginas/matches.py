import streamlit as st

from studymatch import sessao
from studymatch.api import ErroAPI

st.title("Meus matches")
api = sessao.api()

if st.button("Atualizar", icon=":material/refresh:"):
    sessao.invalidar("meus_matches")

try:
    matches = sessao.dados_da_sessao("meus_matches", api.meus_matches)
except ErroAPI as e:
    sessao.mostrar_erro(e)
    st.stop()

sucesso = st.session_state.pop("matches_sucesso", None)
if sucesso:
    st.success(sucesso)


def nome_completo(item):
    return f"{item['nome']} {item['sobrenome'] or ''}".strip()


def cabecalho(item):
    col_nome, col_percentual = st.columns([3, 1], vertical_alignment="center")
    col_nome.subheader(nome_completo(item))
    if item.get("semestre"):
        col_nome.caption(f"{item['semestre']}º semestre")
    col_percentual.metric("Compatibilidade", f"{item['percentual'] or 0}%")
    if item.get("sobre_mim"):
        st.caption(item["sobre_mim"])


def executar(acao, mensagem):
    """Executa a ação na API e recarrega as listas (a busca também muda de situação)."""
    try:
        acao()
    except ErroAPI as e:
        sessao.mostrar_erro(e)
    else:
        sessao.invalidar("meus_matches", "compativeis")
        st.session_state["matches_sucesso"] = mensagem
        st.rerun()


recebidos, enviados, confirmados = matches["recebidos"], matches["enviados"], matches["confirmados"]
aba_recebidos, aba_enviados, aba_confirmados = st.tabs([
    f"Recebidos ({len(recebidos)})", f"Enviados ({len(enviados)})", f"Confirmados ({len(confirmados)})",
])

with aba_recebidos:
    if not recebidos:
        st.info("Nenhum pedido recebido por enquanto.")
    for item in recebidos:
        with st.container(border=True):
            cabecalho(item)
            col_aceitar, col_recusar = st.columns(2)
            if col_aceitar.button("Aceitar", key=f"aceitar_{item['interesse_id']}", type="primary",
                                  icon=":material/check:", width="stretch"):
                executar(lambda: api.responder_interesse(item["interesse_id"], aceitar=True),
                         f"Match confirmado com {item['nome']}! O telefone está em Confirmados.")
            if col_recusar.button("Recusar", key=f"recusar_{item['interesse_id']}", icon=":material/close:",
                                  width="stretch"):
                executar(lambda: api.responder_interesse(item["interesse_id"], aceitar=False),
                         f"Pedido de {item['nome']} recusado.")

with aba_enviados:
    if not enviados:
        st.info("Você ainda não demonstrou interesse em nenhum colega.")
        st.page_link("paginas/buscar.py", label="Buscar colegas", icon=":material/search:")
    for item in enviados:
        with st.container(border=True):
            cabecalho(item)
            if item["status"] == "recusado":
                st.caption("Este colega recusou o seu interesse.")
            else:
                st.caption(":material/schedule: Aguardando resposta.")
                if st.button("Cancelar interesse", key=f"cancelar_{item['interesse_id']}", icon=":material/undo:"):
                    executar(lambda: api.cancelar_interesse(item["interesse_id"]),
                             f"Interesse em {item['nome']} cancelado.")

with aba_confirmados:
    if not confirmados:
        st.info("Quando um match for confirmado, o telefone do colega aparece aqui.")
    for item in confirmados:
        with st.container(border=True):
            cabecalho(item)
            st.markdown(f":material/call: **Telefone:** {item['telefone']}")
