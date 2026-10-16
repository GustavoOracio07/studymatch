"""Rótulos do domínio usados nas telas (apenas apresentação; as regras ficam no Xano)."""

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
