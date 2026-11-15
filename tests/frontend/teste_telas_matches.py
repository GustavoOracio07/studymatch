"""Testes da página Meus matches com streamlit.testing (AppTest) contra a API do Xano.

Cria alunos de teste e apaga todos no final.
Uso: python tests/frontend/teste_telas_matches.py
"""
import os
import pathlib
import sys
from urllib.parse import unquote

RAIZ = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "tests" / "api"))

from apoio import BASE, apagar_aluno, check, novo_aluno, req, resumo  # noqa: E402
from streamlit.testing.v1 import AppTest  # noqa: E402

os.environ.setdefault("XANO_API_URL", BASE)
os.chdir(RAIZ)


def tudo(at):
    return " | ".join([m.value for m in at.markdown] + [s.value for s in at.success] + [i.value for i in at.info]
                      + [c.value for c in at.caption] + [h.value for h in at.subheader])


ta, ida, _, tel_a = novo_aluno("telamatcha")
tb, idb, _, tel_b = novo_aluno("telamatchb")
tc, idc, _, tel_c = novo_aluno("telamatchc")
td, idd, _, tel_d = novo_aluno("telamatchd")
req("PUT", "/minhas_disciplinas", ta, json={"disciplina_ids": [1]})
req("PUT", "/minhas_disciplinas", tb, json={"disciplina_ids": [1]})
disciplina_1 = next(d["nome"] for d in req("GET", "/disciplina").json() if d["id"] == 1)
mi_ba = req("POST", "/match_interesse", tb, json={"usuario_alvo_id": ida}).json()["id"]
mi_ca = req("POST", "/match_interesse", tc, json={"usuario_alvo_id": ida}).json()["id"]
mi_ad = req("POST", "/match_interesse", ta, json={"usuario_alvo_id": idd}).json()["id"]

at = AppTest.from_file(str(RAIZ / "app.py"), default_timeout=90)
at.session_state["token"] = ta
at.run()
at.switch_page("paginas/matches.py").run()
check("abre Meus matches", any(t.value.startswith("Meus matches") for t in at.title), tudo(at))
check("abas com contagem", [t.label for t in at.tabs] == ["Recebidos (2)", "Enviados (1)", "Confirmados (0)"],
      str([t.label for t in at.tabs]))
check("nenhum telefone antes do match", all(tel not in tudo(at) for tel in (tel_b, tel_c, tel_d)), tudo(at))

at.button(key=f"aceitar_{mi_ba}").click().run()
check("aceitar mostra confirmação", "Match confirmado com Teste!" in tudo(at), str([e.value for e in at.error]) + str(at.exception))
check("aceito vai para Confirmados com telefone", f"Telefone: {tel_b}" in tudo(at)
      and [t.label for t in at.tabs][2] == "Confirmados (1)", tudo(at))
links = [e.proto for e in at.get("link_button")]
check("confirmado tem o botão Chamar no WhatsApp com o número do colega",
      [(p.label, p.url.split("?")[0]) for p in links] == [("Chamar no WhatsApp", f"https://wa.me/55{tel_b}")],
      str([(p.label, p.url) for p in links]))
check("mensagem pronta cita a disciplina em comum",
      [unquote(p.url.split("text=")[1]) for p in links]
      == [f"Oi, Teste! Deu match no StudyMatch: temos dificuldade em {disciplina_1}. "
          "Bora marcar um horário para estudar juntos?"], str([p.url for p in links]))

at.button(key=f"recusar_{mi_ca}").click().run()
check("recusar mostra confirmação", "Pedido de Teste recusado." in tudo(at), tudo(at))
check("recusado não mostra telefone", tel_c not in tudo(at) and [t.label for t in at.tabs][0] == "Recebidos (0)",
      tudo(at))

at.button(key=f"cancelar_{mi_ad}").click().run()
check("cancelar interesse mostra confirmação", "Interesse em Teste cancelado." in tudo(at), str([e.value for e in at.error]) + str(at.exception))
check("cancelado sai de Enviados", [t.label for t in at.tabs][1] == "Enviados (0)", str([t.label for t in at.tabs]))

r = req("GET", "/meus_matches", tb)
check("B vê o telefone de A no Xano", [i.get("telefone") for i in r.json()["confirmados"]] == [tel_a], r.text)

for t in (ta, tb, tc, td):
    apagar_aluno(t)
resumo()
