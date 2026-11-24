"""Testes da change chat-match contra a API do Xano.

Cria alunos de teste e apaga todos no final.
Uso: python tests/api/teste_chat.py
"""
from apoio import apagar_aluno, check, novo_aluno, req, resumo

ta, ida, _, _ = novo_aluno("chata")
tb, idb, _, _ = novo_aluno("chatb")
tc, idc, _, _ = novo_aluno("chatc")
td, idd, _, _ = novo_aluno("chatd")

ab = req("POST", "/match_interesse", ta, json={"usuario_alvo_id": idb}).json()["id"]
req("PATCH", f"/match_interesse/{ab}", tb, json={"status": "match"})


def enviar(token, texto, match=ab, **extra):
    return req("POST", "/mensagem", token, json={"match_interesse_id": match, "texto": texto, **extra})


def ler(token, match=ab, **params):
    return req("GET", "/mensagem", token, params={"match_interesse_id": match, **params})


# --- envio e leitura
r = ler(ta)
check("conversa nova vem vazia", r.status_code == 200 and r.json() == [], r.text)
r = enviar(ta, "  Oi!  ", remetente_id=idb)
check("A envia e o texto perde os espaços das pontas", r.status_code == 200 and r.json()["texto"] == "Oi!", r.text)
check("remetente forjado é ignorado", r.json().get("remetente_id") == ida, r.text)
check("resposta tem só os campos previstos", set(r.json()) == {"id", "remetente_id", "texto", "created_at"}, r.text)
m1 = r.json()["id"]
r = enviar(tb, "<b>Olá</b>")
check("B responde", r.status_code == 200 and r.json()["remetente_id"] == idb, r.text)
m2 = r.json()["id"]
r = ler(tb)
check("leitura traz as duas mensagens em ordem",
      [(m["id"], m["remetente_id"], m["texto"]) for m in r.json()] == [(m1, ida, "Oi!"), (m2, idb, "<b>Olá</b>")], r.text)
r = ler(ta, depois_de=m1)
check("depois_de traz só as novas", [m["id"] for m in r.json()] == [m2], r.text)
r = ler(ta, depois_de=m2)
check("sem novas devolve lista vazia", r.status_code == 200 and r.json() == [], r.text)

# --- validação
for nome, texto in (("vazio", ""), ("só espaços", "   "), ("501 caracteres", "a" * 501)):
    r = enviar(ta, texto)
    check(f"texto {nome} -> 400", r.status_code == 400, f"{r.status_code} {r.text}")
r = enviar(ta, "é" * 500)
check("500 caracteres com acento -> 200", r.status_code == 200 and r.json()["texto"] == "é" * 500, r.text[:200])
r = ler(ta)
check("textos inválidos não foram gravados", len(r.json()) == 3, r.text[:200])

# --- acesso
check("C não lê -> 403", ler(tc).status_code == 403)
check("C não envia -> 403", enviar(tc, "x").status_code == 403)
check("ler sem token -> 401", ler(None).status_code == 401)
check("enviar sem token -> 401", enviar(None, "x").status_code == 401)
check("ler match inexistente -> 404", ler(ta, 999999999).status_code == 404)
check("enviar em match inexistente -> 404", enviar(ta, "x", 999999999).status_code == 404)
ac = req("POST", "/match_interesse", ta, json={"usuario_alvo_id": idc}).json()["id"]
check("ler pendente -> 403", ler(ta, ac).status_code == 403)
check("enviar em pendente -> 403", enviar(ta, "x", ac).status_code == 403)
req("PATCH", f"/match_interesse/{ac}", tc, json={"status": "recusado"})
check("ler recusado -> 403", ler(ta, ac).status_code == 403)
check("enviar em recusado -> 403", enviar(ta, "x", ac).status_code == 403)
check("mensagens barradas não foram gravadas", len(ler(ta).json()) == 3)

# --- limite de 50
bd = req("POST", "/match_interesse", tb, json={"usuario_alvo_id": idd}).json()["id"]
req("PATCH", f"/match_interesse/{bd}", td, json={"status": "match"})
ids = [enviar(tb, f"m{i}", bd).json()["id"] for i in range(52)]
check("sem depois_de traz as 50 últimas em ordem", [m["id"] for m in ler(td, bd).json()] == ids[-50:])
check("com depois_de traz as 50 primeiras seguintes",
      [m["id"] for m in ler(td, bd, depois_de=ids[0]).json()] == ids[1:51])
check("mensagens de outra conversa não se misturam", len(ler(ta).json()) == 3)

# --- exclusão da conta
check("A apaga a conta -> 200", apagar_aluno(ta).status_code == 200)
check("B não lê mais a conversa -> 404", ler(tb).status_code == 404)
check("conversa de B com D continua", len(ler(td, bd).json()) == 50)

for t in (tb, tc, td):
    apagar_aluno(t)
resumo()
