import datetime as dt

import streamlit as st

from studymatch import sessao
from studymatch.api import ErroAPI, listar_cursos, listar_disciplinas
from studymatch.dominio import DIAS_SEMANA as DIAS
from studymatch.dominio import descrever_horario

st.title("Meu perfil")
api = sessao.api()

try:
    aluno = sessao.aluno_atual()
    cursos = listar_cursos()
    disciplinas = listar_disciplinas()
    minhas_disciplinas = sessao.dados_da_sessao("minhas_disciplinas", api.minhas_disciplinas)
    minhas_disponibilidades = sessao.dados_da_sessao("minhas_disponibilidades", api.minhas_disponibilidades)
except ErroAPI as e:
    sessao.mostrar_erro(e)
    st.stop()

sucesso = st.session_state.pop("perfil_sucesso", None)
if sucesso:
    st.success(sucesso)

aba_dados, aba_disciplinas, aba_disponibilidade = st.tabs(["Dados", "Disciplinas", "Disponibilidade"])

# --- Dados pessoais
with aba_dados:
    id_por_curso = {c["nome"]: c["id"] for c in cursos}
    curso_por_id = {c["id"]: c["nome"] for c in cursos}
    nomes_cursos = list(id_por_curso)
    curso_atual = curso_por_id.get(aluno.get("curso_id"))

    with st.form("dados"):
        col1, col2 = st.columns(2)
        nome = col1.text_input("Nome *", value=aluno.get("Name") or "")
        sobrenome = col2.text_input("Sobrenome *", value=aluno.get("Sobrenome") or "")
        st.text_input("E-mail", value=aluno.get("email") or "", disabled=True)
        telefone = st.text_input("Telefone *", value=aluno.get("Telefone") or "",
                                 help="Só aparece para quem tiver um match confirmado com você.")
        col3, col4 = st.columns([3, 1])
        curso = col3.selectbox("Curso *", options=nomes_cursos,
                               index=nomes_cursos.index(curso_atual) if curso_atual in nomes_cursos else None)
        semestre = col4.number_input("Semestre *", min_value=1, max_value=12, value=aluno.get("Semestre") or 1, step=1)
        sobre_mim = st.text_area("Sobre mim", value=aluno.get("Sobre_mim") or "")
        st.caption("Se você trocar de curso, suas disciplinas de dificuldade serão removidas.")
        salvar_dados = st.form_submit_button("Salvar dados", type="primary")

    if salvar_dados:
        if not nome.strip() or not sobrenome.strip() or not telefone.strip() or curso is None:
            st.error("Preencha todos os campos marcados com *.")
        else:
            try:
                atualizado = api.atualizar_perfil({
                    "name": nome.strip(),
                    "sobrenome": sobrenome.strip(),
                    "telefone": telefone.strip(),
                    "curso_id": id_por_curso[curso],
                    "semestre": int(semestre),
                    "sobre_mim": sobre_mim.strip(),
                })
            except ErroAPI as e:
                sessao.mostrar_erro(e)
            else:
                if atualizado["curso_id"] != aluno.get("curso_id"):
                    sessao.invalidar("minhas_disciplinas")
                st.session_state["aluno"] = atualizado
                sessao.invalidar("compativeis")
                st.session_state["perfil_sucesso"] = "Dados salvos."
                st.rerun()

# --- Disciplinas de dificuldade (só do próprio curso)
with aba_disciplinas:
    id_por_disciplina = {d["nome"]: d["id"] for d in disciplinas if d["curso_id"] == aluno.get("curso_id")}
    disciplina_por_id = {v: k for k, v in id_por_disciplina.items()}
    atuais = [disciplina_por_id[m["disciplina_id"]] for m in minhas_disciplinas
              if m["disciplina_id"] in disciplina_por_id]

    if not id_por_disciplina:
        st.info("Ainda não há disciplinas cadastradas para o seu curso.")
    else:
        with st.form("disciplinas"):
            escolhidas = st.multiselect("Disciplinas em que tenho dificuldade", options=list(id_por_disciplina),
                                        default=atuais, placeholder="Escolha uma ou mais disciplinas")
            salvar_disciplinas = st.form_submit_button("Salvar disciplinas", type="primary")

        if salvar_disciplinas:
            try:
                novas = api.definir_disciplinas(id_por_disciplina[nome] for nome in escolhidas)
            except ErroAPI as e:
                sessao.mostrar_erro(e)
            else:
                st.session_state["minhas_disciplinas"] = novas
                sessao.invalidar("compativeis")
                st.session_state["perfil_sucesso"] = "Disciplinas salvas."
                st.rerun()

# --- Disponibilidade
with aba_disponibilidade:
    ordem_dias = list(DIAS)
    faixas = sorted(minhas_disponibilidades, key=lambda f: (ordem_dias.index(f["dia_semana"]), f["hora_inicio"]))

    if not faixas:
        st.info("Você ainda não cadastrou horários disponíveis.")
    for faixa in faixas:
        col_texto, col_botao = st.columns([4, 1], vertical_alignment="center")
        col_texto.write(descrever_horario(faixa))
        if col_botao.button("Remover", key=f"remover_disp_{faixa['id']}", icon=":material/delete:"):
            try:
                api.apagar_disponibilidade(faixa["id"])
            except ErroAPI as e:
                sessao.mostrar_erro(e)
            else:
                st.session_state["minhas_disponibilidades"] = [f for f in minhas_disponibilidades if f["id"] != faixa["id"]]
                sessao.invalidar("compativeis")
                st.rerun()

    with st.form("nova_disponibilidade", clear_on_submit=False):
        st.write("**Adicionar horário**")
        col_dia, col_ini, col_fim = st.columns([2, 1, 1])
        dia = col_dia.selectbox("Dia da semana", options=list(DIAS.values()))
        inicio = col_ini.time_input("Início", value=dt.time(9, 0), step=900)
        fim = col_fim.time_input("Fim", value=dt.time(11, 0), step=900)
        adicionar = st.form_submit_button("Adicionar horário", type="primary")

    if adicionar:
        dia_semana = next(chave for chave, rotulo in DIAS.items() if rotulo == dia)
        try:
            nova = api.adicionar_disponibilidade(dia_semana, inicio.strftime("%H:%M"), fim.strftime("%H:%M"))
        except ErroAPI as e:
            sessao.mostrar_erro(e)
        else:
            st.session_state["minhas_disponibilidades"] = minhas_disponibilidades + [nova]
            sessao.invalidar("compativeis")
            st.session_state["perfil_sucesso"] = "Horário adicionado."
            st.rerun()
