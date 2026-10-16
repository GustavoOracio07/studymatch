// Delete a Match_interesse record (only the origin student can withdraw the interest)
query "match_interesse/{match_interesse_id}" verb=DELETE {
  api_group = "Authentication"
  auth = "user"

  input {
    int match_interesse_id? filters=min:1
  }

  stack {
    db.get Match_interesse {
      field_name = "id"
      field_value = $input.match_interesse_id
    } as $match_interesse
  
    precondition ($match_interesse != null) {
      error_type = "notfound"
      error = "Interesse de match não encontrado."
    }
  
    precondition ($match_interesse.usuario_id == $auth.id) {
      error_type = "accessdenied"
      error = "Só o aluno que enviou o interesse pode apagá-lo."
    }
  
    // A confirmed match cannot be undone by one side alone
    precondition ($match_interesse.status == "pendente") {
      error_type = "inputerror"
      error = "Só é possível cancelar interesses pendentes."
    }
  
    db.del Match_interesse {
      field_name = "id"
      field_value = $input.match_interesse_id
    }
  }

  response = null
  guid = "9Lo3apUOI7t_w8T493p-ol-Hyd8"
}