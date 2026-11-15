"""Rótulos do domínio usados nas telas (apenas apresentação; as regras ficam no Xano)."""
import re
import urllib.parse

DIAS_SEMANA = {
    "segunda": "Segunda-feira",
    "terca": "Terça-feira",
    "quarta": "Quarta-feira",
    "quinta": "Quinta-feira",
    "sexta": "Sexta-feira",
    "sabado": "Sábado",
    "domingo": "Domingo",
}


def descrever_horario(faixa):
    return f"{DIAS_SEMANA[faixa['dia_semana']]}, das {faixa['hora_inicio']} às {faixa['hora_fim']}"


def juntar(itens):
    """["A"] -> "A"; ["A", "B"] -> "A e B"; ["A", "B", "C"] -> "A, B e C"."""
    itens = list(itens)
    if len(itens) <= 1:
        return "".join(itens)
    return ", ".join(itens[:-1]) + " e " + itens[-1]


def link_whatsapp(telefone, nome="", disciplinas=()):
    """Link do WhatsApp (wa.me) com uma mensagem pronta, ou None se o telefone não tiver número suficiente.

    Telefones brasileiros sem DDI (10 ou 11 dígitos, ex.: 11973358648) ganham o 55 na frente.
    `disciplinas` são os nomes das disciplinas em comum, citados na mensagem quando houver."""
    digitos = re.sub(r"\D", "", telefone or "")
    if len(digitos) in (10, 11):
        digitos = "55" + digitos
    if len(digitos) < 12:
        return None
    saudacao = f"Oi, {nome}!" if nome else "Oi!"
    motivo = f": temos dificuldade em {juntar(disciplinas)}." if disciplinas else "."
    mensagem = f"{saudacao} Deu match no StudyMatch{motivo} Bora marcar um horário para estudar juntos?"
    return f"https://wa.me/{digitos}?text={urllib.parse.quote(mensagem)}"
