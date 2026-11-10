"""Testes da change foto-perfil contra a API do Xano.

Cria alunos de teste e apaga todos no final.
Uso: python tests/api/teste_foto.py
"""
import io
import random

import requests
from PIL import Image

from apoio import apagar_aluno, check, novo_aluno, req, resumo


def imagem(formato, lado=64):
    """Imagem de ruído (não comprime bem, então o tamanho cresce com o lado)."""
    img = Image.frombytes("RGB", (lado, lado), random.randbytes(lado * lado * 3))
    buf = io.BytesIO()
    img.save(buf, format=formato, quality=100) if formato == "JPEG" else img.save(buf, format=formato)
    return buf.getvalue()


def enviar(token, nome, conteudo, mime):
    return req("POST", "/auth/me/foto", token, files={"foto": (nome, conteudo, mime)})


def abre(url, conteudo):
    """O Xano recodifica a imagem ao guardar, então compara o formato e as dimensões, não os bytes."""
    if not url:
        return False
    r = requests.get(url, timeout=30)
    if r.status_code != 200 or not r.headers.get("content-type", "").startswith("image/"):
        return False
    recebida, enviada = Image.open(io.BytesIO(r.content)), Image.open(io.BytesIO(conteudo))
    return recebida.size == enviada.size


ta, ida, _, _ = novo_aluno("fotoa")
tb, idb, email_b, _ = novo_aluno("fotob")
req("PUT", "/minhas_disciplinas", ta, json={"disciplina_ids": [1]})
req("PUT", "/minhas_disciplinas", tb, json={"disciplina_ids": [1]})

r = req("GET", "/auth/me", ta)
check("perfil sem foto traz foto_url nulo", r.status_code == 200 and "foto_url" in r.json()
      and r.json()["foto_url"] is None and "Foto" not in r.json(), r.text)

png = imagem("PNG")
r = enviar(ta, "foto.png", png, "image/png")
url1 = r.json().get("foto_url") if r.status_code == 200 else None
check("enviar PNG válido -> 200 com foto_url", r.status_code == 200 and url1, r.text)
check("foto_url abre a imagem enviada", abre(url1, png), url1)
check("resposta não traz o objeto Foto", "Foto" not in r.json(), r.text)

jpg = imagem("JPEG")
r = enviar(ta, "outra.jpg", jpg, "image/jpeg")
url2 = r.json().get("foto_url") if r.status_code == 200 else None
check("trocar a foto -> 200 com nova URL", r.status_code == 200 and url2 and url2 != url1, r.text)
check("nova foto abre", abre(url2, jpg), url2)

r = enviar(ta, "doc.pdf", b"%PDF-1.4\n%fake\n", "application/pdf")
check("PDF -> 400 com mensagem", r.status_code == 400 and "JPEG, PNG ou WEBP" in r.text, r.text)
grande = imagem("JPEG", 1200)
assert len(grande) > 2 * 1024 * 1024, len(grande)
r = enviar(ta, "grande.jpg", grande, "image/jpeg")
check("imagem acima de 2 MB -> 400 com mensagem", r.status_code == 400 and "2 MB" in r.text, r.text)
r = req("POST", "/auth/me/foto", ta, files={"outro": ("x.txt", b"x", "text/plain")})
check("envio sem o campo foto -> 400", r.status_code == 400, r.text)
r = req("GET", "/auth/me", ta)
check("foto atual não muda após erros", r.json().get("foto_url") == url2, r.text)

# a foto aparece para os colegas
r = req("GET", "/compativeis", tb)
item = next((c for c in r.json() if c["usuario_id"] == ida), {}) if r.status_code == 200 else {}
check("compativeis traz foto_url do colega", item.get("foto_url") == url2, r.text)
check("compativeis não expõe Foto nem path", "Foto" not in item and "path" not in item, r.text)
req("POST", "/match_interesse", ta, json={"usuario_alvo_id": idb})
r = req("GET", "/meus_matches", tb)
rec = r.json()["recebidos"] if r.status_code == 200 else []
check("meus_matches traz foto_url em pedido pendente, sem telefone",
      [(i["usuario_id"], i.get("foto_url"), "telefone" in i) for i in rec] == [(ida, url2, False)], r.text)
r = req("GET", "/meus_matches", ta)
env = r.json()["enviados"] if r.status_code == 200 else []
check("colega sem foto vem com foto_url nulo", [i.get("foto_url", "ausente") for i in env] == [None], r.text)

# remover
r = req("DELETE", "/auth/me/foto", ta)
check("remover foto -> 200", r.status_code == 200, r.text)
r = req("GET", "/auth/me", ta)
check("após remover, foto_url é nulo", r.json().get("foto_url", "ausente") is None, r.text)
r = req("DELETE", "/auth/me/foto", ta)
check("remover sem ter foto -> 200", r.status_code == 200, r.text)

r = req("POST", "/auth/me/foto", files={"foto": ("foto.png", png, "image/png")})
check("POST foto sem token -> 401", r.status_code == 401, r.text)
r = req("DELETE", "/auth/me/foto")
check("DELETE foto sem token -> 401", r.status_code == 401, r.text)

# a exclusão da conta funciona com foto
r = enviar(tb, "b.png", png, "image/png")
url_b = r.json().get("foto_url") if r.status_code == 200 else None
check("B envia foto", abre(url_b, png), r.text)
r = apagar_aluno(tb)
check("B com foto apaga a conta -> 200", r.status_code == 200, r.text)
r = req("POST", "/auth/login", json={"email": email_b, "password": "senha1234"})
check("login de B passa a falhar", r.status_code != 200, r.text)

apagar_aluno(ta)
resumo()
