"""Testes da change seguranca-backend-xano contra a API do Xano.

Cria alunos de teste e apaga todos no final (DELETE /auth/me).
O plano free do Xano aceita 10 requisições a cada 20 s, então o script espera entre as chamadas.

Uso: python tests/api/teste_seguranca.py
"""
from apoio import apagar_aluno, check, novo_aluno, req, resumo


# --- autenticação
ta, ida, email_a, tel_a = novo_aluno("a")
tb, idb, email_b, tel_b = novo_aluno("b")
r = req("POST", "/auth/login", json={"email": email_a, "password": "senha1234"})
check("login correto devolve token", r.status_code == 200 and "authToken" in r.json(), r.text)
r = req("POST", "/auth/login", json={"email": email_a, "password": "errada123"})
check("senha errada -> 403 msg PT", r.status_code == 403 and "inválidos" in r.text, r.text)
r = req("POST", "/auth/login", json={"email": "naoexiste@studymatch.test", "password": "x"})
check("email inexistente -> 403", r.status_code == 403, r.text)
r = req("POST", "/auth/signup", json={"name": "T", "email": "outro." + email_a, "password": "senha1234",
                                       "sobrenome": "X", "curso_id": 1, "semestre": 2, "telefone": tel_a})
check("telefone duplicado -> 400 msg amigável",
      r.status_code == 400 and "telefone já está cadastrado" in r.text, r.text)
r = req("POST", "/auth/signup", json={"name": "T", "email": email_a, "password": "senha1234",
                                       "sobrenome": "X", "curso_id": 1, "semestre": 2, "telefone": "1"+tel_a})
check("email duplicado -> 400 msg amigável", r.status_code == 400 and "e-mail já está cadastrado" in r.text, r.text)
r = req("GET", "/auth/me", ta)
check("auth/me devolve Name", r.status_code == 200 and r.json().get("Name") == "Teste", r.text)

# --- controle de acesso: disponibilidade
r = req("POST", "/disponibilidade", json={"dia_semana": "segunda", "hora_inicio": "09:00", "hora_fim": "11:00"})
check("POST disponibilidade sem token -> 401", r.status_code == 401, f"{r.status_code} {r.text}")
r = req("POST", "/disponibilidade", tb, json={"usuario_id": ida, "dia_semana": "segunda",
                                              "hora_inicio": "09:00", "hora_fim": "11:00"})
check("dono = token (ignora usuario_id)", r.status_code == 200 and r.json()["usuario_id"] == idb, r.text)
disp_b = r.json()["id"]
r = req("POST", "/disponibilidade", ta, json={"dia_semana": "terca", "hora_inicio": "14:00", "hora_fim": "16:00"})
disp_a = r.json()["id"]
r = req("GET", "/disponibilidade", tb)
check("listagem só do próprio aluno", r.status_code == 200 and all(d["usuario_id"] == idb for d in r.json())
      and len(r.json()) == 1, r.text)
r = req("GET", f"/disponibilidade/{disp_a}", tb)
check("GET disponibilidade alheia -> 403", r.status_code == 403, r.text)
r = req("PATCH", f"/disponibilidade/{disp_a}", tb, json={"hora_fim": "18:00"})
check("PATCH disponibilidade alheia -> 403", r.status_code == 403, r.text)
r = req("PATCH", f"/disponibilidade/{disp_b}", tb, json={"hora_fim": "12:00"})
check("PATCH própria mantém campos não enviados", r.status_code == 200 and r.json()["hora_fim"] == "12:00"
      and r.json()["dia_semana"] == "segunda" and r.json()["hora_inicio"] == "09:00", r.text)
r = req("PATCH", f"/disponibilidade/{disp_b}", tb, json={"hora_fim": "08:00"})
check("PATCH fim < início -> 400", r.status_code == 400, r.text)
r = req("DELETE", f"/disponibilidade/{disp_a}", tb)
check("DELETE disponibilidade alheia -> 403", r.status_code == 403, r.text)
check("registro alheio continua existindo", req("GET", f"/disponibilidade/{disp_a}", ta).status_code == 200)
r = req("DELETE", f"/disponibilidade/{disp_b}", tb)
check("DELETE própria -> 200", r.status_code == 200, r.text)

# --- usuario_disciplina
r = req("POST", "/usuario_disciplina", ta, json={"usuario_id": idb, "disciplina_id": 1})
check("usuario_disciplina dono = token", r.status_code == 200 and r.json()["usuario_id"] == ida, r.text)
ud_a = r.json()["id"]
r = req("GET", "/usuario_disciplina", tb)
check("listagem usuario_disciplina vazia p/ B", r.status_code == 200 and r.json() == [], r.text)
r = req("DELETE", f"/usuario_disciplina/{ud_a}", tb)
check("DELETE usuario_disciplina alheia -> 403", r.status_code == 403, r.text)
r = req("GET", "/usuario_disciplina")
check("GET usuario_disciplina sem token -> 401", r.status_code == 401, r.text)

# --- match_interesse
r = req("POST", "/match_interesse", ta, json={"usuario_alvo_id": ida, "percentual_compatibilidade": 50})
check("interesse em si mesmo -> 400", r.status_code == 400, r.text)
r = req("POST", "/match_interesse", ta, json={"usuario_id": idb, "usuario_alvo_id": idb,
                                              "percentual_compatibilidade": 70})
check("POST interesse origem = token, pendente",
      r.status_code == 200 and r.json()["usuario_id"] == ida and r.json()["status"] == "pendente", r.text)
mi = r.json()["id"]
r = req("PATCH", f"/match_interesse/{mi}", ta, json={"status": "match"})
check("origem não aceita o próprio interesse -> 403", r.status_code == 403, r.text)
r = req("DELETE", f"/match_interesse/{mi}", tb)
check("alvo não apaga interesse -> 403", r.status_code == 403, r.text)
r = req("PATCH", f"/match_interesse/{mi}", tb, json={"status": "match"})
check("alvo aceita -> match", r.status_code == 200 and r.json()["status"] == "match", r.text)
r = req("PATCH", f"/match_interesse/{mi}", tb, json={"status": "recusado"})
check("responder de novo -> 400", r.status_code == 400, r.text)
r = req("GET", "/match_interesse", tb)
check("listagem match só com participação", r.status_code == 200 and
      all(ida in (m["usuario_id"], m["usuario_alvo_id"]) or idb in (m["usuario_id"], m["usuario_alvo_id"])
          for m in r.json()) and len(r.json()) == 1, r.text)

# --- curso / disciplina
r = req("POST", "/curso", ta, json={"nome": "Curso indevido"})
check("member cria curso -> 403", r.status_code == 403, r.text)
r = req("POST", "/curso", json={"nome": "Curso indevido"})
check("criar curso sem token -> 401", r.status_code == 401, r.text)
r = req("DELETE", "/disciplina/1", ta)
check("member apaga disciplina -> 403", r.status_code == 403, r.text)
r = req("GET", "/curso")
check("GET curso público", r.status_code == 200 and len(r.json()) >= 2, r.text)

# --- welcome email
r = req("POST", "/message/send_welcome_email", json={"user_id": ida})
check("welcome email sem token -> 401", r.status_code == 401, r.text)
r = req("POST", "/message/send_welcome_email", tb, json={"user_id": ida})
check("welcome email para outro -> 403", r.status_code == 403, r.text)

# --- exclusão em cascata
req("POST", "/disponibilidade", tb, json={"dia_semana": "quarta", "hora_inicio": "10:00", "hora_fim": "11:00"})
req("POST", "/usuario_disciplina", tb, json={"disciplina_id": 2})
r = apagar_aluno(tb)
check("DELETE auth/me -> 200", r.status_code == 200, r.text)
r = req("POST", "/auth/login", json={"email": email_b, "password": "senha1234"})
check("usuário apagado não loga", r.status_code == 403, r.text)
# limpeza de A (também testa cascata com disponibilidade + disciplina)
r = apagar_aluno(ta)
check("DELETE auth/me (A) -> 200", r.status_code == 200, r.text)

resumo()
