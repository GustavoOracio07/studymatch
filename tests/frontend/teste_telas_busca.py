"""Testes da busca de colegas (página Início) com streamlit.testing (AppTest) contra a API do Xano.

Cria alunos de teste e apaga todos no final.
Uso: python tests/frontend/teste_telas_busca.py
"""
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
    return " | ".join([e.value for e in at.error] + [s.value for s in at.success] + [i.value for i in at.info]
                      + [c.value for c in at.caption])


def abrir_busca(token):
    at = AppTest.from_file(str(RAIZ / "app.py"), default_timeout=90)
    at.session_state["token"] = token
    at.run()
    return at


def aluno_com_disciplinas(tag, disciplinas):
    token, uid, _, _ = novo_aluno(tag, curso=1)
    req("PUT", "/minhas_disciplinas", token, json={"disciplina_ids": disciplinas})
    return token, uid


ta, ida = aluno_com_disciplinas("telabuscaa", [4])
tb, idb = aluno_com_disciplinas("telabuscab", [4])
tc, idc = aluno_com_disciplinas("telabuscac", [4])
td, idd = aluno_com_disciplinas("telabuscad", [])
req("POST", "/match_interesse", tc, json={"usuario_alvo_id": ida})  # C já quer estudar com A

at = abrir_busca(ta)
check("Início mostra os colegas compatíveis", any("Pessoas compatíveis com você" in m.value for m in at.markdown),
      textos(at))
check("mostra o selo de compatibilidade", any("60% de compatibilidade" in m.value for m in at.markdown),
      str([m.value for m in at.markdown]))
check("mostra as disciplinas em comum", any("Projeto de Banco de Dados" in m.value for m in at.markdown),
      str([m.value for m in at.markdown]))

at.button(key=f"interesse_{idb}").click().run()
check("Dar match mostra confirmação", "Interesse enviado para Teste." in textos(at), textos(at))
check("cartão passa a mostrar Interesse enviado", "Interesse enviado. Aguardando resposta." in textos(at), textos(at))
r = req("GET", "/match_interesse", tb)
check("interesse gravado no Xano", any(m["usuario_id"] == ida and m["status"] == "pendente" for m in r.json()), r.text)

check("colega que já tem interesse mostra Aceitar", "Este colega quer estudar com você." in textos(at), textos(at))
at.button(key=f"aceitar_{idc}").click().run()
check("Aceitar interesse confirma o match", "Match confirmado com Teste!" in textos(at), textos(at))

at = abrir_busca(td)
check("lista vazia orienta a completar o perfil", "Nenhum colega compatível por enquanto." in " ".join(i.value for i in at.info),
      textos(at))

for t in (ta, tb, tc, td):
    apagar_aluno(t)
resumo()
