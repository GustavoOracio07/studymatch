"""Início: colegas compatíveis (busca) e resumo do perfil, como no Figma."""
import streamlit as st

from studymatch import sessao, visual
from studymatch.api import ErroAPI, listar_cursos, listar_disciplinas
from studymatch.dominio import DIAS_SEMANA, descrever_horario
from studymatch.visual import esc, html_, icone, linha

ORDENACOES = ["Maior compatibilidade", "Menor compatibilidade", "Nome (A–Z)"]
TODOS_SEMESTRES = "Todos os semestres"

api = sessao.api()

try:
    with st.spinner("Carregando..."):
        aluno = sessao.aluno_atual()
        cursos = {c["id"]: c["nome"] for c in listar_cursos()}
        nome_disciplina = {d["id"]: d["nome"] for d in listar_disciplinas()}
        compativeis = sessao.dados_da_sessao("compativeis", api.compativeis)
        minhas_disciplinas = sessao.dados_da_sessao("minhas_disciplinas", api.minhas_disciplinas)
        minhas_disponibilidades = sessao.dados_da_sessao("minhas_disponibilidades", api.minhas_disponibilidades)
except ErroAPI as e:
    sessao.mostrar_erro(e)
    st.stop()

sigla = visual.sigla_curso(cursos.get(aluno.get("curso_id"), ""))

with visual.hero():
    st.title(f"Olá, {aluno['Name']}! 👋")
    st.markdown("Encontre pessoas com os mesmos interesses e horários que você para estudar junto. "
                "Seu próximo match pode estar a um clique!")


def resumo_horarios(faixas):
    return "; ".join(f"{DIAS_SEMANA[f['dia_semana']].split('-')[0]} {f['hora_inicio']}–{f['hora_fim']}" for f in faixas)


@st.dialog("Perfil do colega", width="medium")
def ver_perfil(colega):
    html_(f'<div class="sm-info">{visual.avatar(colega["nome"], colega["sobrenome"], colega["usuario_id"], grande=True)}'
          f'<div><div class="sm-nome-linha"><span class="sm-nome">{esc(colega["nome"])} {esc(colega["sobrenome"])}'
          f'</span>{visual.selo(colega["percentual"])}</div>'
          + linha("curso", f"{esc(sigla)} • {esc(colega['semestre'])}º semestre")
          + "</div></div>")
    st.markdown("**Disciplinas em comum**")
    st.markdown("\n".join(f"- {nome_disciplina.get(i, i)}" for i in colega["disciplinas_comuns"]))
    st.markdown("**Horários em comum**")
    if colega["horarios_comuns"]:
        st.markdown("\n".join(f"- {descrever_horario(h)}" for h in colega["horarios_comuns"]))
    else:
        st.caption("Nenhum horário em comum.")
    st.markdown("**Sobre mim**")
    st.caption(colega.get("sobre_mim") or "Este colega ainda não escreveu nada.")
    st.caption("O telefone aparece em Meus matches depois que o match for confirmado.")


principal, lateral = st.columns([2.7, 1], gap="large")

# --- Colegas compatíveis
with principal:
    with st.container(horizontal=True, vertical_alignment="bottom", gap="small"):
        busca = st.text_input("Buscar por matéria", placeholder="Buscar por matéria...", label_visibility="collapsed",
                              icon=":material/search:", width=230)
        semestre = st.selectbox("Semestre", [TODOS_SEMESTRES] + [f"{n}º semestre" for n in range(1, 13)],
                                label_visibility="collapsed", width=180)
        if st.button("Atualizar lista", icon=":material/refresh:"):
            sessao.invalidar("compativeis")
            st.rerun()

    lista = compativeis
    if busca.strip():
        termo = busca.strip().lower()
        lista = [c for c in lista
                 if any(termo in nome_disciplina.get(i, "").lower() for i in c["disciplinas_comuns"])]
    if semestre != TODOS_SEMESTRES:
        lista = [c for c in lista if c.get("semestre") == int(semestre.split("º")[0])]

    col_titulo, col_ordem = st.columns([2.2, 1], vertical_alignment="center")
    html_(f'<div class="sm-titulo-secao">Pessoas compatíveis com você '
          f'<span class="sm-contador">{len(lista)} resultado{"s" if len(lista) != 1 else ""}</span></div>', col_titulo)
    ordem = col_ordem.selectbox("Ordenar por", ORDENACOES, label_visibility="collapsed")
    if ordem == "Menor compatibilidade":
        lista = sorted(lista, key=lambda c: c["percentual"])
    elif ordem == "Nome (A–Z)":
        lista = sorted(lista, key=lambda c: f"{c['nome']} {c['sobrenome'] or ''}".lower())

    sucesso = st.session_state.pop("busca_sucesso", None)
    if sucesso:
        st.success(sucesso)

    if not compativeis:
        st.info("Nenhum colega compatível por enquanto. A busca considera as disciplinas em que você tem "
                "dificuldade e os seus horários livres.")
        st.page_link("paginas/perfil.py", label="Revisar disciplinas e horários em Meu perfil",
                     icon=":material/person:")
    elif not lista:
        st.info("Nenhum colega encontrado com esses filtros.")

    for colega in lista:
        with st.container(key=f"cartao_colega_{colega['usuario_id']}"):
            info, sobre = st.columns([1.15, 1], gap="medium")
            disciplinas = ", ".join(esc(nome_disciplina.get(i, f"Disciplina {i}")) for i in colega["disciplinas_comuns"])
            horarios = esc(resumo_horarios(colega["horarios_comuns"])) or "Nenhum horário em comum"
            html_(
                '<div class="sm-info">'
                + visual.avatar(colega["nome"], colega["sobrenome"], colega["usuario_id"])
                + '<div><div class="sm-nome-linha">'
                + f'<span class="sm-nome">{esc(colega["nome"])} {esc(colega["sobrenome"])}</span>'
                + visual.selo(colega["percentual"]) + "</div>"
                + linha("curso", f"{esc(sigla)} • {esc(colega['semestre'])}º semestre")
                + linha("livro", disciplinas)
                + linha("relogio", horarios)
                + "</div></div>",
                info,
            )
            with sobre:
                html_('<div class="sm-sobre-titulo">Sobre mim</div>'
                      f'<div class="sm-sobre-texto">{esc(colega.get("sobre_mim")) or "—"}</div>')
                situacao = colega["situacao"]
                acao = None
                with st.container(horizontal=True, horizontal_alignment="right", gap="small"):
                    if st.button("Ver perfil", key=f"ver_{colega['usuario_id']}"):
                        ver_perfil(colega)
                    if situacao == "nenhum":
                        acao = st.button("Dar match", key=f"interesse_{colega['usuario_id']}", type="primary",
                                         icon=":material/favorite:", icon_position="right")
                    elif situacao == "recebido":
                        acao = st.button("Aceitar interesse", key=f"aceitar_{colega['usuario_id']}", type="primary",
                                         icon=":material/handshake:", icon_position="right")
                if situacao == "recebido":
                    st.caption("Este colega quer estudar com você.")
                elif situacao == "enviado":
                    st.caption(":material/schedule: Interesse enviado. Aguardando resposta.")
                elif situacao == "match":
                    st.caption(":material/check_circle: Match confirmado! Veja o contato em Meus matches.")
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

# --- Resumo do perfil
with lateral, st.container(key="painel_perfil"):
    col_t, col_e = st.columns([1.5, 1], vertical_alignment="center")
    html_('<div class="sm-titulo-secao">Seu perfil</div>', col_t)
    with col_e:
        st.page_link("paginas/perfil.py", label="Editar", icon=":material/edit_square:")

    nomes_minhas = [nome_disciplina.get(m["disciplina_id"], "") for m in minhas_disciplinas]
    itens = [True, bool(minhas_disciplinas), bool(minhas_disponibilidades), bool(aluno.get("Sobre_mim")),
             bool(aluno.get("Telefone"))]
    completo = round(100 * sum(itens) / len(itens))
    ok = f'<span class="sm-ok">{icone("check", 16)}</span>'
    falta = f'<span class="sm-cinza">{icone("seta", 16)}</span>'

    html_(
        '<div class="sm-perfil-topo">'
        + visual.avatar(aluno.get("Name"), aluno.get("Sobrenome"), aluno.get("id"))
        + f'<div><div class="sm-nome">{esc(aluno.get("Name"))} {esc(aluno.get("Sobrenome"))}</div>'
        + f'<div class="sm-sobre-texto">{esc(sigla)} • {esc(aluno.get("Semestre"))}º semestre</div></div></div>'
        + f'<div class="sm-sobre-texto">Seu perfil está {completo}% completo</div>'
        + f'<div class="sm-barra"><div style="width:{completo}%"></div></div>'
        + f'<div class="sm-item-perfil"><span>{icone("livro")} Matérias <span class="sm-cinza">'
          f'({len(minhas_disciplinas)})</span></span>{ok if minhas_disciplinas else falta}</div>'
        + f'<div class="sm-item-perfil"><span>{icone("relogio")} Horários <span class="sm-cinza">'
          f'({len(minhas_disponibilidades)})</span></span>{ok if minhas_disponibilidades else falta}</div>'
        + f'<div class="sm-item-perfil"><span>{icone("usuario")} Sobre mim</span>'
          f'{ok if aluno.get("Sobre_mim") else falta}</div>'
        + f'<div class="sm-item-perfil"><span>{icone("telefone")} Forma de contato</span>'
          f'{ok if aluno.get("Telefone") else falta}</div>'
        + '<div class="sm-resumo-titulo">Resumo do seu perfil</div>'
        + f'<div class="sm-resumo-rotulo">{icone("livro")} Matérias</div>'
        + f'<div class="sm-resumo-valor">{esc(", ".join(nomes_minhas)) or "Nenhuma ainda"}</div>'
        + f'<div class="sm-resumo-rotulo">{icone("relogio")} Horários disponíveis</div>'
        + f'<div class="sm-resumo-valor">{esc(resumo_horarios(minhas_disponibilidades)) or "Nenhum ainda"}</div>'
        + f'<div class="sm-resumo-rotulo">{icone("telefone")} Telefone</div>'
        + f'<div class="sm-resumo-valor">{esc(aluno.get("Telefone"))}</div>'
    )
    if completo < 100:
        st.page_link("paginas/perfil.py", label="Completar perfil", icon=":material/arrow_forward:")
