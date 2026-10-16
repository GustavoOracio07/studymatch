// Edit a Disponibilidade record owned by the authenticated user
query "disponibilidade/{disponibilidade_id}" verb=PATCH {
  api_group = "Authentication"
  auth = "user"

  input {
    int disponibilidade_id? filters=min:1
    enum dia_semana? {
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
  
    text hora_inicio? filters=trim
    text hora_fim? filters=trim
  }

  stack {
    db.get Disponibilidade {
      field_name = "id"
      field_value = $input.disponibilidade_id
    } as $atual
  
    precondition ($atual != null) {
      error_type = "notfound"
      error = "Disponibilidade não encontrada."
    }
  
    precondition ($atual.usuario_id == $auth.id) {
      error_type = "accessdenied"
      error = "Você só pode alterar as suas próprias disponibilidades."
    }
  
    // Merge the sent (non-empty) fields over the current record (the owner never changes)
    var $novo {
      value = {
        dia_semana : $input.dia_semana|first_notempty:$atual.dia_semana
        hora_inicio: $input.hora_inicio|first_notempty:$atual.hora_inicio
        hora_fim   : $input.hora_fim|first_notempty:$atual.hora_fim
      }
    }
  
    function.run "StudyMatch/validar_disponibilidade" {
      input = {
        user_id    : $auth.id
        dia_semana : $novo.dia_semana
        hora_inicio: $novo.hora_inicio
        hora_fim   : $novo.hora_fim
        ignorar_id : $atual.id
      }
    }
  
    db.patch Disponibilidade {
      field_name = "id"
      field_value = $input.disponibilidade_id
      data = $novo
    } as $disponibilidade
  }

  response = $disponibilidade
  guid = "fKxnWwxSjWRDRGysh9Piz4xWvns"
}