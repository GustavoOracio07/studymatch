// Valida uma faixa de disponibilidade: formato HH:MM, fim depois do início e sem sobreposição com outra faixa do aluno no mesmo dia
function "StudyMatch/validar_disponibilidade" {
  input {
    int user_id
    text dia_semana
    text hora_inicio
    text hora_fim
  
    // Id da faixa sendo editada (não conta como sobreposição com ela mesma)
    int ignorar_id?
  }

  stack {
    precondition (("/^([01][0-9]|2[0-3]):[0-5][0-9]$/"|regex_matches:$input.hora_inicio) && ("/^([01][0-9]|2[0-3]):[0-5][0-9]$/"|regex_matches:$input.hora_fim)) {
      error_type = "inputerror"
      error = "Use horários no formato HH:MM."
    }
  
    precondition ($input.hora_fim > $input.hora_inicio) {
      error_type = "inputerror"
      error = "O horário de fim deve ser depois do horário de início"
    }
  
    db.query Disponibilidade {
      where = $db.Disponibilidade.usuario_id == $input.user_id && $db.Disponibilidade.dia_semana == $input.dia_semana && $db.Disponibilidade.id != $input.ignorar_id && $db.Disponibilidade.hora_inicio < $input.hora_fim && $db.Disponibilidade.hora_fim > $input.hora_inicio
      return = {type: "exists"}
    } as $sobreposta
  
    precondition ($sobreposta == false) {
      error_type = "inputerror"
      error = "Este horário se sobrepõe a outra disponibilidade sua."
    }
  }

  response = null
  guid = "YFuoo8o8HsHGa6qEjLwNW2_BOME"
}