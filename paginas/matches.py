import streamlit as st

from studymatch import sessao, visual
from studymatch.api import ErroAPI, listar_cursos
from studymatch.visual import esc, html_, linha

ORDENACOES = ["Maior compatibilidade", "Menor compatibilidade", "Nome (A–Z)"]

api = sessao.api()

with visual.hero():
    st.title("Meus matches 💜")

try:
    with st.spinner("Carregando..."):
        aluno = sessao.aluno_atual()
        cursos = {c["id"]: c["nome"] for c in listar_cursos()}
        matches = sessao.dados_da_sessao("meus_matches", api.meus_matches)
except ErroAPI as e:
    sessao.mostrar_erro(e)
    st.stop()

# Os colegas sugeridos são sempre do mesmo curso do aluno
sigla = visual.sigla_curso(cursos.get(aluno.get("curso_id"), ""))

with st.container(horizontal=True, vertical_alignment="bottom", gap="small"):
    busca = st.text_input("Buscar match", placeholder="Buscar match...", label_visibility="collapsed",
                          icon=":material/search:", width=300)
    ordem = st.selectbox("Ordenar por", ORDENACOES, label_visibility="collapsed", width=230)
    if st.button("Atualizar", icon=":material/refresh:"):
        sessao.invalidar("meus_matches")
        st.rerun()

sucesso = st.session_state.pop("matches_sucesso", None)
if sucesso:
    st.success(sucesso)


def preparar(itens):
    termo = busca.strip().lower()
    if termo:
        itens = [i for i in itens if termo in f"{i['nome']} {i['sobrenome'] or ''}".lower()]
    if ordem == "Menor compatibilidade":
        return sorted(itens, key=lambda i: i["percentual"] or 0)
    if ordem == "Nome (A–Z)":
        return sorted(itens, key=lambda i: f"{i['nome']} {i['sobrenome'] or ''}".lower())
    return sorted(itens, key=lambda i: i["percentual"] or 0, reverse=True)


def titulo(texto, quantidade):
    html_(f'<div class="sm-titulo-secao">{texto} <span class="sm-contador">{quantidade} '
          f'resultado{"s" if quantidade != 1 else ""}</span></div>')


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


def cartao(item, meio_html, acoes=None):
    """Cartão no formato do Figma: dados do colega | situação/contato | sobre mim e botões."""
    with st.container(key=f"cartao_match_{item['interesse_id']}"):
        col_info, col_meio, col_sobre = st.columns([1.35, 0.9, 1.1], gap="medium")
        html_(
            '<div class="sm-info">'
            + visual.avatar(item["nome"], item["sobrenome"], item["usuario_id"])
            + '<div><div class="sm-nome-linha">'
            + f'<span class="sm-nome">{esc(item["nome"])} {esc(item["sobrenome"])}</span>'
            + visual.selo(item["percentual"]) + "</div>"
            + linha("curso", f"{esc(sigla)} • {esc(item['semestre'])}º semestre")
            + "</div></div>",
            col_info,
        )
        html_(meio_html, col_meio)
        with col_sobre:
            html_('<div class="sm-sobre-titulo">Sobre mim</div>'
                  f'<div class="sm-sobre-texto">{esc(item.get("sobre_mim")) or "—"}</div>')
            if acoes:
                with st.container(horizontal=True, horizontal_alignment="right", gap="small"):
                    acoes()


recebidos = preparar(matches["recebidos"])
enviados = preparar(matches["enviados"])
confirmados = preparar(matches["confirmados"])
aba_recebidos, aba_enviados, aba_confirmados = st.tabs([
    f"Recebidos ({len(matches['recebidos'])})",
    f"Enviados ({len(matches['enviados'])})",
    f"Confirmados ({len(matches['confirmados'])})",
])

with aba_recebidos:
    titulo("Pessoas que querem estudar com você", len(recebidos))
    if not recebidos:
        st.info("Nenhum pedido recebido por enquanto.")
    for item in recebidos:
        def botoes(item=item):
            if st.button("Recusar", key=f"recusar_{item['interesse_id']}", icon=":material/close:"):
                executar(lambda: api.responder_interesse(item["interesse_id"], aceitar=False),
                         f"Pedido de {item['nome']} recusado.")
            if st.button("Aceitar", key=f"aceitar_{item['interesse_id']}", type="primary", icon=":material/check:"):
                executar(lambda: api.responder_interesse(item["interesse_id"], aceitar=True),
                         f"Match confirmado com {item['nome']}! O telefone está em Confirmados.")

        cartao(item, linha("coracao", "Quer estudar com você", "sm-destaque"), botoes)

with aba_enviados:
    titulo("Interesses que você enviou", len(enviados))
    if not enviados:
        st.info("Você ainda não demonstrou interesse em nenhum colega.")
        st.page_link("paginas/inicio.py", label="Buscar colegas no Início", icon=":material/search:")
    for item in enviados:
        if item["status"] == "recusado":
            cartao(item, linha("relogio", "Este colega recusou o seu interesse."))
        else:
            def botoes(item=item):
                if st.button("Cancelar interesse", key=f"cancelar_{item['interesse_id']}", icon=":material/undo:"):
                    executar(lambda: api.cancelar_interesse(item["interesse_id"]),
                             f"Interesse em {item['nome']} cancelado.")

            cartao(item, linha("relogio", "Aguardando resposta.", "sm-destaque"), botoes)

with aba_confirmados:
    titulo("Pessoas com quem você deu match", len(confirmados))
    if not confirmados:
        st.info("Quando um match for confirmado, o telefone do colega aparece aqui.")
    for item in confirmados:
        cartao(item, linha("check", "Match confirmado", "sm-destaque")
               + linha("telefone", f"Telefone: {esc(item['telefone'])}"))
