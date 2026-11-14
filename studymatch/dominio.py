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


def link_whatsapp(telefone, nome=""):
    """Link do WhatsApp (wa.me) com uma mensagem pronta, ou None se o telefone não tiver número suficiente.

    Telefones brasileiros sem DDI (10 ou 11 dígitos, ex.: 11973358648) ganham o 55 na frente."""
    digitos = re.sub(r"\D", "", telefone or "")
    if len(digitos) in (10, 11):
        digitos = "55" + digitos
    if len(digitos) < 12:
        return None
    saudacao = f"Oi, {nome}!" if nome else "Oi!"
    mensagem = f"{saudacao} Deu match no StudyMatch. Bora marcar um horário para estudar juntos?"
    return f"https://wa.me/{digitos}?text={urllib.parse.quote(mensagem)}"
