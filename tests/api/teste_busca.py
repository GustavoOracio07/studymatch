"""Testes da change busca-compativeis contra a API do Xano.

Cria alunos de teste e apaga todos no final.
Uso: python tests/api/teste_busca.py
"""
from apoio import apagar_aluno, check, novo_aluno, req, resumo


def preparar(tag, curso, disciplinas, faixas):
    token, uid, _, _ = novo_aluno(tag, curso=curso)
    req("PUT", "/minhas_disciplinas", token, json={"disciplina_ids": disciplinas})
    for dia, ini, fim in faixas:
        req("POST", "/disponibilidade", token, json={"dia_semana": dia, "hora_inicio": ini, "hora_fim": fim})
    return token, uid


# Disciplinas 1-5 são do curso 1; 6-10 do curso 2
ta, ida = preparar("buscaa", 1, [1, 2], [("segunda", "09:00", "11:00")])
tb, idb = preparar("buscab", 1, [1], [])                                    # 60: disciplinas sim, horário não
tc, idc = preparar("buscac", 1, [1, 2], [("segunda", "09:00", "11:00")])   # 100: tudo igual
td, idd = preparar("buscad", 1, [1], [("segunda", "10:00", "14:00")])      # 80: metade do horário
te, ide = preparar("buscae", 1, [3], [("segunda", "09:00", "11:00")])      # sem disciplina em comum
tf, idf = preparar("buscaf", 2, [6], [("segunda", "09:00", "11:00")])      # outro curso
todos = [ta, tb, tc, td, te, tf]

r = req("GET", "/compativeis", ta)
lista = r.json() if r.status_code == 200 else []
por_id = {c["usuario_id"]: c for c in lista}
check("GET compativeis -> 200", r.status_code == 200, r.text)
check("percentual 100 (tudo igual)", por_id.get(idc, {}).get("percentual") == 100, r.text)
check("percentual 80 (metade do horário)", por_id.get(idd, {}).get("percentual") == 80, r.text)
check("percentual 60 (sem horário em comum)", por_id.get(idb, {}).get("percentual") == 60, r.text)
check("ordenado do mais para o menos compatível",
      [c["usuario_id"] for c in lista if c["usuario_id"] in (idb, idc, idd)] == [idc, idd, idb], r.text)
check("sem disciplina em comum não aparece", ide not in por_id, r.text)
check("aluno de outro curso não aparece", idf not in por_id, r.text)
check("o próprio aluno não aparece", ida not in por_id, r.text)
check("sem telefone nem e-mail", all("Telefone" not in c and "email" not in c and "telefone" not in c for c in lista), r.text)
check("disciplinas e horários em comum", por_id.get(idd, {}).get("disciplinas_comuns") == [1]
      and por_id.get(idd, {}).get("horarios_comuns") == [{"dia_semana": "segunda", "hora_inicio": "10:00", "hora_fim": "11:00"}],
      r.text)
check("situação inicial é nenhum", por_id.get(idb, {}).get("situacao") == "nenhum", r.text)

r = req("GET", "/compativeis", tb)
check("cálculo simétrico (B vê A com 60)", {c["usuario_id"]: c for c in r.json()}.get(ida, {}).get("percentual") == 60,
      r.text)
r = req("GET", "/compativeis")
check("GET compativeis sem token -> 401", r.status_code == 401, r.text)

# --- interesse
r = req("POST", "/match_interesse", ta, json={"usuario_alvo_id": idb, "percentual_compatibilidade": 100})
check("percentual calculado pelo backend (ignora o do cliente)",
      r.status_code == 200 and r.json().get("percentual_compatibilidade") == 60 and r.json().get("status") == "pendente",
      r.text)
mi = r.json().get("id")
r = req("POST", "/match_interesse", ta, json={"usuario_alvo_id": idb})
check("interesse repetido -> 400", r.status_code == 400 and "já demonstrou interesse" in r.text, r.text)

r = req("GET", "/compativeis", ta)
check("A vê B como enviado", {c["usuario_id"]: c for c in r.json()}.get(idb, {}).get("situacao") == "enviado", r.text)
r = req("GET", "/compativeis", tb)
check("B vê A como recebido", {c["usuario_id"]: c for c in r.json()}.get(ida, {}).get("situacao") == "recebido"
      and {c["usuario_id"]: c for c in r.json()}.get(ida, {}).get("interesse_id") == mi, r.text)

r = req("POST", "/match_interesse", tb, json={"usuario_alvo_id": ida})
check("interesse cruzado vira match no mesmo registro",
      r.status_code == 200 and r.json().get("id") == mi and r.json().get("status") == "match", r.text)
r = req("GET", "/match_interesse", ta)
entre_eles = [m for m in r.json() if {m["usuario_id"], m["usuario_alvo_id"]} == {ida, idb}]
check("continua só um registro entre os dois", len(entre_eles) == 1, r.text)
r = req("POST", "/match_interesse", ta, json={"usuario_alvo_id": idb})
check("já têm match -> 400", r.status_code == 400 and "já têm um match" in r.text, r.text)
r = req("GET", "/compativeis", ta)
check("A vê B como match", {c["usuario_id"]: c for c in r.json()}.get(idb, {}).get("situacao") == "match", r.text)

r = req("POST", "/match_interesse", ta, json={"usuario_alvo_id": 99999999})
check("aluno inexistente -> 404", r.status_code == 404 and "Aluno não encontrado" in r.text, r.text)
r = req("POST", "/match_interesse", ta, json={"usuario_alvo_id": ida})
check("interesse em si mesmo -> 400", r.status_code == 400, r.text)

for t in todos:
    apagar_aluno(t)
resumo()
