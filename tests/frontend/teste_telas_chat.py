"""Testes da página Conversa com streamlit.testing (AppTest) contra a API do Xano.

Cria alunos de teste e apaga todos no final.
Uso: python tests/frontend/teste_telas_chat.py
"""
import os
import pathlib
import sys
import time

RAIZ = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "tests" / "api"))
sys.path.insert(0, str(RAIZ))

from apoio import BASE, apagar_aluno, check, novo_aluno, req, resumo  # noqa: E402
from streamlit.testing.v1 import AppTest  # noqa: E402

from studymatch.api import MSG_LIMITE, ErroAPI, XanoAPI  # noqa: E402

os.environ.setdefault("XANO_API_URL", BASE)
os.chdir(RAIZ)

ta, ida, _, _ = novo_aluno("telachata")
tb, idb, _, _ = novo_aluno("telachatb")
tc, idc, _, _ = novo_aluno("telachatc")
td, idd, _, _ = novo_aluno("telachatd")
ab = req("POST", "/match_interesse", ta, json={"usuario_alvo_id": idb}).json()["id"]
req("PATCH", f"/match_interesse/{ab}", tb, json={"status": "match"})
ac = req("POST", "/match_interesse", ta, json={"usuario_alvo_id": idc}).json()["id"]
da = req("POST", "/match_interesse", td, json={"usuario_alvo_id": ida}).json()["id"]
time.sleep(20)  # janela do limite do plano free

at = AppTest.from_file(str(RAIZ / "app.py"), default_timeout=90)
at.session_state["token"] = ta
at.run()
at.switch_page("paginas/conversa.py").run()
check("sem colega escolhido pede para ir a Meus matches", any("Escolha um colega" in i.value for i in at.info))

time.sleep(20)
at.switch_page("paginas/matches.py").run()
conversar = [b.key for b in at.button if b.label == "Conversar"]
check("só o match confirmado tem Conversar", conversar == [f"conversar_{ab}"], str(conversar))
at.button(key=f"conversar_{ab}").click().run()
check("Conversar abre a página com o nome do colega", [t.value for t in at.title] == ["Conversa com Teste"],
      str([t.value for t in at.title]) + str(at.exception))

# O AppTest volta a Meus matches na próxima execução (não acompanha o st.switch_page): fixa a página da conversa
time.sleep(20)
at.switch_page("paginas/conversa.py").run()
at.chat_input[0].set_value("Oi!").run()
check("mensagem enviada aparece na conversa", "Oi!" in [t.value for t in at.text],
      str([t.value for t in at.text]) + str([e.value for e in at.error]) + str(at.exception))
r = req("GET", "/mensagem", tb, params={"match_interesse_id": ab})
check("mensagem chegou ao Xano com A como remetente",
      [(m["remetente_id"], m["texto"]) for m in r.json()] == [(ida, "Oi!")], r.text)

req("POST", "/mensagem", tb, json={"match_interesse_id": ab, "texto": "<b>oi</b> **x**"})
at.run()
check("mensagem recebida aparece literal, sem HTML nem Markdown", "<b>oi</b> **x**" in [t.value for t in at.text]
      and all("<b>oi</b>" not in m.value for m in at.markdown), str([t.value for t in at.text]))
check("mensagens mostram Você e o nome do colega",
      [m.value for m in at.markdown if "sm-conversa-autor" in m.value]
      == [f'<div class="sm-conversa-autor">{n}</div>' for n in ("Você", "Teste")], str([m.value for m in at.markdown]))
check("nenhuma mensagem se repete", [t.value for t in at.text] == ["Oi!", "<b>oi</b> **x**"],
      str([t.value for t in at.text]))


def limite(self, *args):
    raise ErroAPI(MSG_LIMITE, 429)


original, XanoAPI.mensagens = XanoAPI.mensagens, limite
at.run()
AVISO = "Atualizando a conversa..."
check("no limite, mostra aviso discreto e mantém as mensagens",
      AVISO in [c.value for c in at.caption] and not at.warning and len(at.text) == 2, str([c.value for c in at.caption]))
time.sleep(20)
at.chat_input[0].set_value("No limite").run()
check("mensagem enviada aparece mesmo com a busca no limite", [t.value for t in at.text][2:] == ["No limite"],
      str([t.value for t in at.text]) + str([e.value for e in at.error]))
req("POST", "/mensagem", tb, json={"match_interesse_id": ab, "texto": "Resposta"})
XanoAPI.mensagens = original
time.sleep(20)
at.run()
check("depois do limite, o aviso some e nada se perde nem se repete",
      AVISO not in [c.value for c in at.caption]
      and [t.value for t in at.text] == ["Oi!", "<b>oi</b> **x**", "No limite", "Resposta"],
      str([t.value for t in at.text]))

for t in (ta, tb, tc, td):
    apagar_aluno(t)
resumo()
