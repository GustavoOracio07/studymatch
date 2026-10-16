"""Testes da change perfil-aluno contra a API do Xano.

Cria alunos de teste e apaga todos no final.
Uso: python tests/api/teste_perfil.py
"""
from apoio import apagar_aluno, check, novo_aluno, req, resumo

# Disciplinas 1-5 são de ADS (curso 1); 6-10 de Ciência da Computação (curso 2)
ta, ida, email_a, tel_a = novo_aluno("perfa", curso=1)
tb, idb, email_b, tel_b = novo_aluno("perfb", curso=1)

# --- perfil
r = req("GET", "/auth/me", ta)
me = r.json()
check("auth/me traz o perfil completo", r.status_code == 200 and me.get("Sobrenome") == "PERFA"
      and me.get("curso_id") == 1 and me.get("Semestre") == 3 and me.get("Telefone") == tel_a, r.text)
check("auth/me não traz a senha", "Password" not in me and "password" not in me, r.text)

perfil = {"name": "Ana", "sobrenome": "Souza", "telefone": tel_a, "curso_id": 1, "semestre": 4,
          "sobre_mim": "Gosto de estudar à noite"}
r = req("PATCH", "/auth/me", ta, json=perfil)
check("PATCH auth/me atualiza", r.status_code == 200 and r.json().get("Name") == "Ana"
      and r.json().get("Semestre") == 4 and r.json().get("Sobre_mim") == "Gosto de estudar à noite", r.text)
check("PATCH auth/me não devolve a senha", "Password" not in r.json(), r.text)
r = req("PATCH", "/auth/me", ta, json={**perfil, "semestre": 13})
check("semestre 13 -> 400", r.status_code == 400 and "entre 1 e 12" in r.text, r.text)
r = req("PATCH", "/auth/me", ta, json={**perfil, "telefone": tel_b})
check("telefone de outro aluno -> 400", r.status_code == 400 and "telefone já está cadastrado" in r.text, r.text)
r = req("PATCH", "/auth/me", ta, json={**perfil, "curso_id": 999})
check("curso inexistente -> 400", r.status_code == 400 and "Curso não encontrado" in r.text, r.text)
r = req("PATCH", "/auth/me", json=perfil)
check("PATCH auth/me sem token -> 401", r.status_code == 401, r.text)

# --- disciplinas
r = req("PUT", "/minhas_disciplinas", ta, json={"disciplina_ids": [1, 2, 2]})
check("PUT minhas_disciplinas define a lista (sem repetir)", r.status_code == 200
      and sorted(d["disciplina_id"] for d in r.json()) == [1, 2], r.text)
r = req("PUT", "/minhas_disciplinas", ta, json={"disciplina_ids": [1, 6]})
check("disciplina de outro curso na lista -> 400", r.status_code == 400 and "do seu curso" in r.text, r.text)
r = req("GET", "/usuario_disciplina", ta)
check("lista anterior continua igual", sorted(d["disciplina_id"] for d in r.json()) == [1, 2], r.text)
r = req("POST", "/usuario_disciplina", ta, json={"disciplina_id": 7})
check("POST disciplina de outro curso -> 400", r.status_code == 400 and "do seu curso" in r.text, r.text)
r = req("POST", "/usuario_disciplina", ta, json={"disciplina_id": 1})
check("POST disciplina repetida -> 400", r.status_code == 400 and "já está na sua lista" in r.text, r.text)
r = req("POST", "/usuario_disciplina", ta, json={"disciplina_id": 3})
check("POST disciplina do curso -> 200", r.status_code == 200, r.text)
ud = r.json().get("id")
r = req("PATCH", f"/usuario_disciplina/{ud}", ta, json={"disciplina_id": 8})
check("PATCH para disciplina de outro curso -> 400", r.status_code == 400, r.text)

r = req("PATCH", "/auth/me", ta, json={**perfil, "curso_id": 2})
check("troca de curso -> 200", r.status_code == 200 and r.json().get("curso_id") == 2, r.text)
r = req("GET", "/usuario_disciplina", ta)
check("troca de curso remove as disciplinas antigas", r.status_code == 200 and r.json() == [], r.text)
r = req("PUT", "/minhas_disciplinas", ta, json={"disciplina_ids": [6, 7]})
check("disciplinas do novo curso aceitas", r.status_code == 200 and len(r.json()) == 2, r.text)
r = req("PUT", "/minhas_disciplinas", ta, json={"disciplina_ids": []})
check("lista vazia limpa as disciplinas", r.status_code == 200 and r.json() == [], r.text)


# --- disponibilidade
def disp(dia, ini, fim, token=ta):
    return req("POST", "/disponibilidade", token, json={"dia_semana": dia, "hora_inicio": ini, "hora_fim": fim})


r = disp("segunda", "09:00", "11:00")
check("faixa válida", r.status_code == 200, r.text)
d1 = r.json().get("id")
r = disp("segunda", "11:00", "13:00")
check("faixa encostada é permitida", r.status_code == 200, r.text)
r = disp("segunda", "10:00", "12:00")
check("faixa sobreposta -> 400", r.status_code == 400 and "se sobrepõe" in r.text, r.text)
r = disp("segunda", "08:00", "14:00")
check("faixa que engloba outras -> 400", r.status_code == 400 and "se sobrepõe" in r.text, r.text)
r = disp("terca", "10:00", "12:00")
check("mesmo horário em outro dia é permitido", r.status_code == 200, r.text)
r = disp("segunda", "10:00", "12:00", token=tb)
check("mesmo horário de outro aluno é permitido", r.status_code == 200, r.text)
r = disp("quarta", "9h", "11:00")
check("formato inválido -> 400", r.status_code == 400 and "HH:MM" in r.text, r.text)
r = disp("quarta", "24:00", "24:30")
check("hora 24:00 -> 400", r.status_code == 400 and "HH:MM" in r.text, r.text)
r = disp("quarta", "23:00", "01:00")
check("atravessar a meia-noite -> 400", r.status_code == 400 and "fim deve ser depois" in r.text, r.text)
r = req("PATCH", f"/disponibilidade/{d1}", ta, json={"hora_fim": "10:30"})
check("editar sem conflitar consigo mesma", r.status_code == 200 and r.json().get("hora_fim") == "10:30", r.text)
r = req("PATCH", f"/disponibilidade/{d1}", ta, json={"hora_fim": "12:00"})
check("editar criando sobreposição -> 400", r.status_code == 400 and "se sobrepõe" in r.text, r.text)

apagar_aluno(ta)
apagar_aluno(tb)
resumo()
