import streamlit as st

from studymatch import sessao
from studymatch.api import ErroAPI, listar_disciplinas
from studymatch.dominio import descrever_horario

st.title("Buscar colegas")
st.caption("Colegas do seu curso com dificuldade nas mesmas disciplinas, do mais para o menos compatível.")
api = sessao.api()

if st.button("Atualizar lista", icon=":material/refresh:"):
    sessao.invalidar("compativeis")

try:
    compativeis = sessao.dados_da_sessao("compativeis", api.compativeis)
    nome_disciplina = {d["id"]: d["nome"] for d in listar_disciplinas()}
except ErroAPI as e:
    sessao.mostrar_erro(e)
    st.stop()

sucesso = st.session_state.pop("busca_sucesso", None)
if sucesso:
    st.success(sucesso)

if not compativeis:
    st.info(
        "Nenhum colega compatível por enquanto. A busca considera as disciplinas em que você tem dificuldade "
        "e os seus horários livres."
    )
    st.page_link("paginas/perfil.py", label="Revisar disciplinas e horários em Meu perfil", icon=":material/person:")
    st.stop()

for colega in compativeis:
    with st.container(border=True):
        col_nome, col_percentual = st.columns([3, 1], vertical_alignment="center")
        col_nome.subheader(f"{colega['nome']} {colega['sobrenome'] or ''}".strip())
        col_nome.caption(f"{colega['semestre']}º semestre" if colega.get("semestre") else "")
        col_percentual.metric("Compatibilidade", f"{colega['percentual']}%")
        st.progress(colega["percentual"] / 100)

        disciplinas = ", ".join(nome_disciplina.get(i, f"Disciplina {i}") for i in colega["disciplinas_comuns"])
        st.markdown(f"**Disciplinas em comum:** {disciplinas}")
        if colega["horarios_comuns"]:
            st.markdown("**Horários em comum:** " + "; ".join(descrever_horario(h) for h in colega["horarios_comuns"]))
        else:
            st.markdown("**Horários em comum:** nenhum")
        if colega.get("sobre_mim"):
            st.caption(colega["sobre_mim"])

        situacao = colega["situacao"]
        acao = None
        if situacao == "nenhum":
            acao = st.button("Tenho interesse", key=f"interesse_{colega['usuario_id']}", type="primary",
                             icon=":material/favorite:")
        elif situacao == "recebido":
            st.info("Este colega quer estudar com você.")
            acao = st.button("Aceitar interesse", key=f"aceitar_{colega['usuario_id']}", type="primary",
                             icon=":material/handshake:")
        elif situacao == "enviado":
            st.caption(":material/schedule: Interesse enviado. Aguardando resposta.")
        elif situacao == "match":
            st.success("Match confirmado! Veja o contato em Meus matches.")
        elif situacao == "recusado":
            st.caption("Interesse recusado.")

        if acao:
            try:
                interesse = api.demonstrar_interesse(colega["usuario_id"])
            except ErroAPI as e:
                sessao.mostrar_erro(e)
            else:
                virou_match = interesse["status"] == "match"
                colega["situacao"] = "match" if virou_match else "enviado"
                colega["interesse_id"] = interesse["id"]
                sessao.invalidar("meus_matches")
                st.session_state["busca_sucesso"] = (
                    f"Match confirmado com {colega['nome']}!" if virou_match
                    else f"Interesse enviado para {colega['nome']}."
                )
                st.rerun()
