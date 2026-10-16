"""Funções de apoio para os testes de API contra o Xano.

O plano free do Xano aceita 10 requisições a cada 20 s, então `req` espera entre as chamadas
e repete quando recebe 429.
"""
import os
import random
import time

import requests

BASE = os.environ.get("XANO_API_URL", "https://x8ki-letl-twmt.n7.xano.io/api:r4ixWYjD")

_ultima = [0.0]
_placar = {"ok": 0, "falhas": 0}


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
    return req("DELETE", "/auth/me", token)


def resumo():
    print(f"\n{_placar['ok']} ok, {_placar['falhas']} falhas")
    raise SystemExit(1 if _placar["falhas"] else 0)
