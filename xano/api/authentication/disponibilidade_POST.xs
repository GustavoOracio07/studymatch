// Add a Disponibilidade record for the authenticated user
query disponibilidade verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
    enum dia_semana {
      values = [
        "segunda"
        "terca"
        "quarta"
        "quinta"
        "sexta"
        "sabado"
        "domingo"
      ]
    }
  
    text hora_inicio filters=trim
    text hora_fim filters=trim
  }

  stack {
    precondition ($input.hora_fim > $input.hora_inicio) {
      error_type = "inputerror"
      error = "O horário de fim deve ser depois do horário de início"
    }
  
    // The owner is always the authenticated user
    db.add Disponibilidade {
      data = {
        created_at : "now"
        usuario_id : $auth.id
        dia_semana : $input.dia_semana
        hora_inicio: $input.hora_inicio
        hora_fim   : $input.hora_fim
      }
    } as $disponibilidade
  }

  response = $disponibilidade
  guid = "d0WE9f45wCAN1rekcyJRxxCVf2w"
}