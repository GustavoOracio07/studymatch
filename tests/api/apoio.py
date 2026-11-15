"""Funções de apoio para os testes de API contra o Xano.

O plano free do Xano aceita 10 requisições a cada 20 s, então `req` espera entre as chamadas
e repete quando recebe 429.
"""
import atexit
import os
import random
import time

import requests

BASE = os.environ.get("XANO_API_URL", "https://x8ki-letl-twmt.n7.xano.io/api:r4ixWYjD")

_ultima = [0.0]
_placar = {"ok": 0, "falhas": 0}
_criados = []  # tokens dos alunos criados neste script e ainda não apagados


def registrar(token):
    """Anota um aluno criado fora de `novo_aluno` (ex.: pela tela) para ser apagado no fim do script."""
    if token and token not in _criados:
        _criados.append(token)


@atexit.register
def _limpar():
    """Apaga os alunos que sobraram, mesmo se o teste parou no meio (erro, assert ou Ctrl+C)."""
    for token in list(_criados):
        try:
            apagar_aluno(token)
        except Exception as e:  # sem rede, por exemplo: avisa e segue
            print("aviso: não consegui apagar um aluno de teste:", e)


def check(nome, cond, extra=""):
    if cond:
        _placar["ok"] += 1
        print("OK  ", nome)
    else:
        _placar["falhas"] += 1
        print("FAIL", nome, extra)


def req(method, path, token=None, **kw):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    for _ in range(5):
        espera = 2.1 - (time.time() - _ultima[0])
        if espera > 0:
            time.sleep(espera)
        _ultima[0] = time.time()
        r = requests.request(method, BASE + path, headers=headers, timeout=30, **kw)
        if r.status_code != 429:
            if path == "/auth/signup" and r.status_code == 200:
                registrar(r.json().get("authToken"))
            return r
        time.sleep(21)
    return r


def novo_aluno(tag, curso=1, semestre=3):
    """Cadastra um aluno de teste e devolve (token, user_id, email, telefone)."""
    n = random.randint(10**7, 10**8 - 1)
    email = f"teste.{tag}.{n}@studymatch.test"
    telefone = f"119{n}"
    r = req("POST", "/auth/signup", json={
        "name": "Teste", "email": email, "password": "senha1234", "sobrenome": tag.upper(),
        "curso_id": curso, "semestre": semestre, "telefone": telefone,
    })
    assert r.status_code == 200, r.text
    return r.json()["authToken"], r.json()["user_id"], email, telefone


def apagar_aluno(token):
    r = req("DELETE", "/auth/me", token)
    if r.status_code in (200, 401) and token in _criados:  # 401: a conta já não existe
        _criados.remove(token)
    return r


def resumo():
    print(f"\n{_placar['ok']} ok, {_placar['falhas']} falhas")
    raise SystemExit(1 if _placar["falhas"] else 0)
