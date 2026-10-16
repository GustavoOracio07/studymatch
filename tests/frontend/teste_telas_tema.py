"""Testes do botão de modo claro/escuro com streamlit.testing (AppTest).

Cria um aluno de teste e apaga no final.
Uso: python tests/frontend/teste_telas_tema.py
"""
import os
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "tests" / "api"))

from apoio import BASE, apagar_aluno, check, novo_aluno, resumo  # noqa: E402
from streamlit.testing.v1 import AppTest  # noqa: E402

os.environ.setdefault("XANO_API_URL", BASE)
os.chdir(RAIZ)


def botao_tema(at):
    return at.button(key="alternar_tema")


at = AppTest.from_file(str(RAIZ / "app.py"), default_timeout=90)
at.run()
check("visitante vê o botão Modo escuro", botao_tema(at).label == "Modo escuro")
botao_tema(at).click().run()
check("clicar ativa o modo escuro", at.session_state["tema_escuro"] is True and botao_tema(at).label == "Modo claro")
at.switch_page("paginas/cadastro.py").run()
check("modo escuro continua no Criar conta", at.session_state["tema_escuro"] is True
      and botao_tema(at).label == "Modo claro")

token, _, _, _ = novo_aluno("tema")
at.session_state["token"] = token
at.run()
check("botão fica no menu lateral do aluno", any(b.key == "alternar_tema" for b in at.sidebar.button))
at.switch_page("paginas/perfil.py").run()
check("modo escuro continua ao trocar de página", at.session_state["tema_escuro"] is True)
at.switch_page("paginas/sair.py").run()
check("modo escuro continua depois de sair", "token" not in at.session_state and at.session_state["tema_escuro"] is True)
botao_tema(at).click().run()
check("clicar de novo volta ao modo claro", at.session_state["tema_escuro"] is False
      and botao_tema(at).label == "Modo escuro")

apagar_aluno(token)
resumo()
