"""Testes da change meus-matches contra a API do Xano.

Cria alunos de teste e apaga todos no final.
Uso: python tests/api/teste_matches.py
"""
from apoio import apagar_aluno, check, novo_aluno, req, resumo

ta, ida, _, tel_a = novo_aluno("matcha")
tb, idb, _, tel_b = novo_aluno("matchb")
tc, idc, _, tel_c = novo_aluno("matchc")
td, idd, _, tel_d = novo_aluno("matchd")

req("POST", "/match_interesse", tb, json={"usuario_alvo_id": ida})   # B -> A (pendente)
r = req("POST", "/match_interesse", ta, json={"usuario_alvo_id": idc})  # A -> C
mi_ac = r.json()["id"]
req("PATCH", f"/match_interesse/{mi_ac}", tc, json={"status": "recusado"})  # C recusa
r = req("POST", "/match_interesse", ta, json={"usuario_alvo_id": idd})  # A -> D
mi_ad = r.json()["id"]

r = req("GET", "/meus_matches", ta)
m = r.json()
check("GET meus_matches -> 200 com as três listas", r.status_code == 200 and set(m) == {"recebidos", "enviados", "confirmados"},
      r.text)
check("pedido de B aparece em recebidos", [i["usuario_id"] for i in m["recebidos"]] == [idb], r.text)
check("recebido traz dados do colega", m["recebidos"][0].get("sobrenome") == "MATCHB" and "percentual" in m["recebidos"][0],
      r.text)
check("enviados traz pendente e recusado",
      sorted((i["usuario_id"], i["status"]) for i in m["enviados"]) == sorted([(idc, "recusado"), (idd, "pendente")]), r.text)
check("sem telefone em recebidos e enviados", all("telefone" not in i and "Telefone" not in i
                                                    for i in m["recebidos"] + m["enviados"]), r.text)
check("nenhum confirmado ainda", m["confirmados"] == [], r.text)

# A aceita o pedido de B
mi_ba = m["recebidos"][0]["interesse_id"]
r = req("PATCH", f"/match_interesse/{mi_ba}", ta, json={"status": "match"})
check("A aceita o pedido de B", r.status_code == 200 and r.json()["status"] == "match", r.text)
r = req("GET", "/meus_matches", ta)
m = r.json()
check("match aparece em confirmados de A com telefone de B",
      [(i["usuario_id"], i.get("telefone")) for i in m["confirmados"]] == [(idb, tel_b)], r.text)
check("recebidos de A fica vazio", m["recebidos"] == [], r.text)
r = req("GET", "/meus_matches", tb)
check("B vê o telefone de A em confirmados",
      [(i["usuario_id"], i.get("telefone")) for i in r.json()["confirmados"]] == [(ida, tel_a)], r.text)
r = req("GET", "/meus_matches", tc)
check("C (recusou) não vê telefone de A", all("telefone" not in i for i in r.json()["enviados"] + r.json()["recebidos"])
      and r.json()["confirmados"] == [], r.text)

# cancelar
r = req("DELETE", f"/match_interesse/{mi_ba}", tb)
check("origem não desfaz match confirmado -> 400", r.status_code == 400 and "pendentes" in r.text, r.text)
r = req("DELETE", f"/match_interesse/{mi_ad}", ta)
check("origem cancela interesse pendente -> 200", r.status_code == 200, r.text)
r = req("GET", "/meus_matches", ta)
check("cancelado sai de enviados", idd not in [i["usuario_id"] for i in r.json()["enviados"]], r.text)

# órfão: B apaga a conta
apagar_aluno(tb)
r = req("GET", "/meus_matches", ta)
check("match com conta apagada é ignorado", r.status_code == 200 and r.json()["confirmados"] == [], r.text)

r = req("GET", "/meus_matches")
check("GET meus_matches sem token -> 401", r.status_code == 401, r.text)

# exclusão da conta apaga os interesses de match (origem ou alvo, qualquer status)
te, ide, _, _ = novo_aluno("matche")
tf, idf, _, _ = novo_aluno("matchf")
tg, idg, _, _ = novo_aluno("matchg")
th, idh, _, _ = novo_aluno("matchh")
mi_ef = req("POST", "/match_interesse", te, json={"usuario_alvo_id": idf}).json()["id"]
req("PATCH", f"/match_interesse/{mi_ef}", tf, json={"status": "match"})          # E e F: match confirmado
req("POST", "/match_interesse", te, json={"usuario_alvo_id": idg})               # E -> G pendente (enviado)
req("POST", "/match_interesse", th, json={"usuario_alvo_id": ide})               # H -> E pendente (recebido)
r = apagar_aluno(te)
check("E apaga a conta -> 200", r.status_code == 200, r.text)
for nome, token in (("F (match)", tf), ("G (recebeu de E)", tg), ("H (enviou para E)", th)):
    r = req("GET", "/match_interesse", token)
    check(f"interesse com E apagado para {nome}",
          r.status_code == 200 and all(ide not in (m["usuario_id"], m["usuario_alvo_id"]) for m in r.json()), r.text)
r = req("GET", "/meus_matches", tf)
check("F não tem mais o match com E em meus_matches", r.json()["confirmados"] == [], r.text)
for token in (tf, tg, th):
    apagar_aluno(token)

for t in (ta, tc, td):
    apagar_aluno(t)
resumo()
