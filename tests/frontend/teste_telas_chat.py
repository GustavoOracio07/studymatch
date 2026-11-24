"""Testes da página Conversa com streamlit.testing (AppTest) contra a API do Xano.

Cria alunos de teste e apaga todos no final.
Uso: python tests/frontend/teste_telas_chat.py
"""
import datetime as dt
import html
import os
import pathlib
import re
import sys
import time

RAIZ = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "tests" / "api"))
sys.path.insert(0, str(RAIZ))

from apoio import BASE, apagar_aluno, check, novo_aluno, req, resumo  # noqa: E402
from streamlit.testing.v1 import AppTest  # noqa: E402

from studymatch.api import MSG_LIMITE, ErroAPI, XanoAPI  # noqa: E402
from studymatch.visual import baloes, hora_mensagem, topo_conversa  # noqa: E402

os.environ.setdefault("XANO_API_URL", BASE)
os.chdir(RAIZ)


def corpo(at):
    return "".join(h.proto.body for h in at.get("html"))


def textos(at):
    return [html.unescape(t) for t in re.findall(r'<div class="sm-balao-texto">(.*?)</div>', corpo(at), re.S)]


# --- apresentação, sem rede
BRT = dt.timezone(dt.timedelta(hours=-3))
ms = int(dt.datetime(2026, 11, 24, 23, 38, tzinfo=BRT).timestamp() * 1000)
check("hora de Brasília, mesmo já sendo outro dia em UTC",
      hora_mensagem(ms, dt.datetime(2026, 11, 24, 23, 50, tzinfo=BRT)) == "23:38")
check("mensagem de outro dia mostra a data",
      hora_mensagem(ms, dt.datetime(2026, 11, 25, 8, tzinfo=BRT)) == "24/11 23:38")
COLEGA = {"usuario_id": 2, "nome": "Ana", "sobrenome": "Lima", "foto_url": None, "disciplinas": ["SQL", "Redes"]}
MSG = [{"id": 1, "remetente_id": 2, "texto": "<b>a</b>\n\n**b**", "created_at": ms}]
check("sem foto, mostra as iniciais", "AL" in baloes(MSG, COLEGA, 1) and "AL" in topo_conversa(COLEGA))
check("quebra de linha e HTML ficam literais", "&lt;b&gt;a&lt;/b&gt;\n\n**b**" in baloes(MSG, COLEGA, 1))
check("cabeçalho mostra as disciplinas", "SQL e Redes" in topo_conversa(COLEGA))
check("sem disciplinas em comum, não mostra a linha", "Match de" not in topo_conversa({**COLEGA, "disciplinas": []}))
com_foto = {**COLEGA, "foto_url": "data:image/jpeg;base64,AAAA"}
check("a foto não se repete nos balões", "base64" not in baloes(MSG, com_foto, 1)
      and "sm-balao-foto" in baloes(MSG, com_foto, 1))

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
check("Conversar abre a página com o nome do colega", "Conversa com Teste" in corpo(at),
      corpo(at)[-500:] + str(at.exception))

# O AppTest volta a Meus matches na próxima execução (não acompanha o st.switch_page): fixa a página da conversa
time.sleep(20)
at.switch_page("paginas/conversa.py").run()
at.chat_input[0].set_value("Oi!").run()
check("mensagem enviada aparece na conversa", "Oi!" in textos(at),
      str(textos(at)) + str([e.value for e in at.error]) + str(at.exception))
r = req("GET", "/mensagem", tb, params={"match_interesse_id": ab})
check("mensagem chegou ao Xano com A como remetente",
      [(m["remetente_id"], m["texto"]) for m in r.json()] == [(ida, "Oi!")], r.text)

req("POST", "/mensagem", tb, json={"match_interesse_id": ab, "texto": "<b>oi</b> **x**"})
at.run()
check("mensagem recebida aparece literal, sem HTML nem Markdown", "<b>oi</b> **x**" in textos(at)
      and "<b>oi</b>" not in corpo(at), str(textos(at)))
check("a minha mensagem fica à direita e a do colega à esquerda",
      re.findall(r'class="sm-mensagem sm-mensagem-(minha|colega)', corpo(at)) == ["minha", "colega"], corpo(at)[-500:])
check("nenhuma mensagem se repete", textos(at) == ["Oi!", "<b>oi</b> **x**"],
      str(textos(at)))


def limite(self, *args):
    raise ErroAPI(MSG_LIMITE, 429)


original, XanoAPI.mensagens = XanoAPI.mensagens, limite
at.run()
AVISO = "Atualizando a conversa..."
check("no limite, mostra aviso discreto e mantém as mensagens",
      AVISO in [c.value for c in at.caption] and not at.warning and len(textos(at)) == 2, str([c.value for c in at.caption]))
time.sleep(20)
at.chat_input[0].set_value("No limite").run()
check("mensagem enviada aparece mesmo com a busca no limite", textos(at)[2:] == ["No limite"],
      str(textos(at)) + str([e.value for e in at.error]))
req("POST", "/mensagem", tb, json={"match_interesse_id": ab, "texto": "Resposta"})
XanoAPI.mensagens = original
time.sleep(20)
at.run()
check("depois do limite, o aviso some e nada se perde nem se repete",
      AVISO not in [c.value for c in at.caption]
      and textos(at) == ["Oi!", "<b>oi</b> **x**", "No limite", "Resposta"],
      str(textos(at)))

for t in (ta, tb, tc, td):
    apagar_aluno(t)
resumo()
