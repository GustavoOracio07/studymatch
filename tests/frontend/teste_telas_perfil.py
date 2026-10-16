"""Testes da página Meu perfil com streamlit.testing (AppTest) contra a API do Xano.

Cria um aluno de teste e apaga no final.
Uso: python tests/frontend/teste_telas_perfil.py
"""
import datetime as dt
import os
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "tests" / "api"))

from apoio import BASE, apagar_aluno, check, novo_aluno, req, resumo  # noqa: E402
from streamlit.testing.v1 import AppTest  # noqa: E402

os.environ.setdefault("XANO_API_URL", BASE)
os.chdir(RAIZ)


def textos(at):
    return " | ".join([e.value for e in at.error] + [s.value for s in at.success] + [i.value for i in at.info])


def botao(at, rotulo):
    return next(b for b in at.button if b.label == rotulo)


token, user_id, email, telefone = novo_aluno("telaperfil", curso=1)

at = AppTest.from_file(str(RAIZ / "app.py"), default_timeout=60)
at.session_state["token"] = token
at.run()
at.switch_page("paginas/perfil.py").run()
check("abre Meu perfil", any(t.value == "Meu perfil" for t in at.title), textos(at))
check("dados vêm preenchidos", next(w for w in at.text_input if w.label == "Sobrenome *").value == "TELAPERFIL")

# --- dados
next(w for w in at.text_area if w.label == "Sobre mim").input("Prefiro estudar de manhã")
next(w for w in at.number_input if w.label == "Semestre *").set_value(5)
botao(at, "Salvar dados").click().run()
check("salvar dados mostra sucesso", "Dados salvos." in textos(at), textos(at))
r = req("GET", "/auth/me", token)
check("dados gravados no Xano", r.json().get("Semestre") == 5 and r.json().get("Sobre_mim") == "Prefiro estudar de manhã",
      r.text)

# --- disciplinas: só as do curso 1 aparecem
multi = at.multiselect[0]
check("só aparecem disciplinas do próprio curso",
      "Fundamentos de SQL" in multi.options and "Cálculo I" not in multi.options, str(multi.options))
multi.set_value(["Fundamentos de SQL", "Engenharia de Software"])
botao(at, "Salvar disciplinas").click().run()
check("salvar disciplinas mostra sucesso", "Disciplinas salvas." in textos(at), textos(at))
r = req("GET", "/usuario_disciplina", token)
check("disciplinas gravadas no Xano", sorted(d["disciplina_id"] for d in r.json()) == [1, 2], r.text)

# --- disponibilidade
check("sem horários mostra aviso", "Você ainda não cadastrou horários disponíveis." in textos(at), textos(at))
dia = next(s for s in at.selectbox if s.label == "Dia da semana")
dia.set_value("Segunda-feira")
next(t for t in at.time_input if t.label == "Início").set_value(dt.time(9, 0))
next(t for t in at.time_input if t.label == "Fim").set_value(dt.time(11, 0))
botao(at, "Adicionar horário").click().run()
check("adicionar horário mostra sucesso", "Horário adicionado." in textos(at), textos(at))
check("horário aparece na lista", any("Segunda-feira, das 09:00 às 11:00" in m.value for m in at.markdown),
      str([m.value for m in at.markdown]))

next(t for t in at.time_input if t.label == "Início").set_value(dt.time(10, 0))
next(t for t in at.time_input if t.label == "Fim").set_value(dt.time(12, 0))
botao(at, "Adicionar horário").click().run()
check("faixa sobreposta mostra o erro da API",
      "Este horário se sobrepõe a outra disponibilidade sua." in textos(at), textos(at))

botao(at, "Remover").click().run()
check("remover horário", not any("Segunda-feira, das 09:00 às 11:00" in m.value for m in at.markdown))
r = req("GET", "/disponibilidade", token)
check("horário removido no Xano", r.json() == [], r.text)

apagar_aluno(token)
resumo()
