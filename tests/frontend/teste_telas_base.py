"""Testes das telas de login, cadastro e logout com streamlit.testing (AppTest) contra a API do Xano.

Cria contas de teste e apaga todas no final.
Uso: python tests/frontend/teste_telas_base.py
"""
import os
import pathlib
import random
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "tests" / "api"))

from apoio import BASE, apagar_aluno, check, novo_aluno, resumo  # noqa: E402
from streamlit.testing.v1 import AppTest  # noqa: E402

os.environ.setdefault("XANO_API_URL", BASE)
os.chdir(RAIZ)


def app():
    at = AppTest.from_file(str(RAIZ / "app.py"), default_timeout=60)
    at.run()
    return at


def textos(at):
    return " | ".join([t.value for t in at.title] + [e.value for e in at.error] + [w.value for w in at.warning])


def enviar(at, rotulo):
    next(b for b in at.button if b.label == rotulo).click().run()


def campo(at, rotulo):
    return next(w for w in list(at.text_input) + list(at.text_area) if w.label.startswith(rotulo))


# --- visitante
at = app()
check("visitante vê a tela Entrar", any(t.value == "StudyMatch" for t in at.title) and "Olá" not in textos(at), textos(at))

enviar(at, "Entrar")
check("campos vazios pedem preenchimento", "Preencha o e-mail e a senha." in textos(at), textos(at))

# --- cadastro pela tela
n = random.randint(10**7, 10**8 - 1)
email = f"teste.tela.{n}@studymatch.test"
at.switch_page("paginas/cadastro.py").run()
check("abre a tela Criar conta", any(t.value == "Criar conta" for t in at.title), textos(at))
campo(at, "Nome").input("Tela")
campo(at, "Sobrenome").input("Teste")
campo(at, "E-mail").input(email)
campo(at, "Senha").input("senha1234")
campo(at, "Telefone").input(f"117{n}")
at.selectbox[0].select_index(0)
enviar(at, "Criar conta")
check("cadastro entra logado no Início", any(t.value == "Olá, Tela!" for t in at.title), textos(at))
token_tela = at.session_state["token"]

# --- logout
at.switch_page("paginas/sair.py").run()
check("sair limpa o token", "token" not in at.session_state)
check("sair volta para Entrar com aviso", "Você saiu da sua conta." in textos(at), textos(at))

# --- login pela tela
campo(at, "E-mail").input(email)
campo(at, "Senha").input("senhaerrada1")
enviar(at, "Entrar")
check("senha errada mostra a mensagem da API", "E-mail ou senha inválidos." in textos(at), textos(at))
campo(at, "Senha").input("senha1234")
enviar(at, "Entrar")
check("login correto leva ao Início", any(t.value == "Olá, Tela!" for t in at.title), textos(at))

# --- telefone duplicado
token_outro, _, _, tel_outro = novo_aluno("outro")
at = app()
at.switch_page("paginas/cadastro.py").run()
campo(at, "Nome").input("Dup")
campo(at, "Sobrenome").input("Teste")
campo(at, "E-mail").input(f"teste.dup.{n}@studymatch.test")
campo(at, "Senha").input("senha1234")
campo(at, "Telefone").input(tel_outro)
at.selectbox[0].select_index(0)
enviar(at, "Criar conta")
check("telefone repetido mostra a mensagem da API", "Este telefone já está cadastrado." in textos(at), textos(at))

# --- sessão expirada
at = app()
at.session_state["token"] = "token-invalido"
at.run()
check("token inválido volta para Entrar com aviso", "Sua sessão expirou. Entre de novo." in textos(at), textos(at))

apagar_aluno(token_tela)
apagar_aluno(token_outro)
resumo()
