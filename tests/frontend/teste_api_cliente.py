"""Testes do cliente da API (studymatch/api.py) com respostas simuladas, sem rede.

Uso: python tests/frontend/teste_api_cliente.py
"""
import json
import pathlib
import sys

import requests

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from studymatch.api import MSG_LIMITE, MSG_REDE, MSG_SESSAO_EXPIRADA, ErroAPI, XanoAPI  # noqa: E402


class RespostaFalsa:
    def __init__(self, status, corpo=None):
        self.status_code = status
        self.content = json.dumps(corpo).encode() if corpo is not None else b""

    def json(self):
        return json.loads(self.content)


class HttpFalso:
    def __init__(self, resposta=None, erro=None):
        self.resposta, self.erro, self.chamadas = resposta, erro, []

    def request(self, metodo, url, headers=None, **kwargs):
        self.chamadas.append((metodo, url, headers, kwargs))
        if self.erro:
            raise self.erro
        return self.resposta


falhas = 0


def check(nome, cond):
    global falhas
    print("OK  " if cond else "FAIL", nome)
    falhas += not cond


def erro_de(http, token=None):
    try:
        XanoAPI(token, base="https://x", http=http, esperar=lambda s: None).eu()
    except ErroAPI as e:
        return e
    return None


http = HttpFalso(RespostaFalsa(200, {"authToken": "t", "user_id": 1}))
r = XanoAPI(base="https://x/", http=http).login("a@b.c", "s")
check("login devolve o JSON", r == {"authToken": "t", "user_id": 1})
check("monta URL sem barra dupla", http.chamadas[0][1] == "https://x/auth/login")
check("sem token não envia Authorization", http.chamadas[0][2] == {})

http = HttpFalso(RespostaFalsa(200, {"id": 1}))
XanoAPI("abc", base="https://x", http=http).eu()
check("com token envia Bearer", http.chamadas[0][2] == {"Authorization": "Bearer abc"})

e = erro_de(HttpFalso(RespostaFalsa(403, {"code": "ERROR_CODE_ACCESS_DENIED", "message": "E-mail ou senha inválidos."})))
check("mensagem de erro vem da API", e and e.mensagem == "E-mail ou senha inválidos." and e.status == 403)

http = HttpFalso(RespostaFalsa(429, {"message": "Whoa there!"}))
e = erro_de(http)
check("429 vira mensagem amigável", e and e.mensagem == MSG_LIMITE and e.status == 429)
check("429 é repetido antes de desistir", len(http.chamadas) == 4)


class HttpLimiteDepoisOk(HttpFalso):
    def request(self, *args, **kwargs):
        self.chamadas.append(args)
        return RespostaFalsa(429) if len(self.chamadas) == 1 else RespostaFalsa(200, {"id": 7})


esperas = []
check("depois do 429 a repetição funciona",
      XanoAPI("t", base="https://x", http=HttpLimiteDepoisOk(), esperar=esperas.append).eu() == {"id": 7}
      and esperas == [2])

e = erro_de(HttpFalso(RespostaFalsa(401, {"message": "Invalid token"})), token="velho")
check("401 com token = sessão expirada", e and e.mensagem == MSG_SESSAO_EXPIRADA and e.status == 401)

e = erro_de(HttpFalso(erro=requests.ConnectionError("sem rede")))
check("erro de rede vira mensagem amigável", e and e.mensagem == MSG_REDE)

e = erro_de(HttpFalso(RespostaFalsa(500)))
check("erro sem corpo tem mensagem genérica", e and "500" in e.mensagem)

http = HttpFalso(RespostaFalsa(200, {}))
XanoAPI("t", base="https://x", http=http).definir_disciplinas(i for i in [1, 2])
check("definir_disciplinas usa PUT com lista",
      http.chamadas[0][:2] == ("PUT", "https://x/minhas_disciplinas") and http.chamadas[0][3]["json"] == {"disciplina_ids": [1, 2]})

http = HttpFalso(RespostaFalsa(200))
check("resposta vazia devolve None", XanoAPI("t", base="https://x", http=http)._req("DELETE", "/x") is None)

print(f"\n{falhas} falhas")
raise SystemExit(1 if falhas else 0)
