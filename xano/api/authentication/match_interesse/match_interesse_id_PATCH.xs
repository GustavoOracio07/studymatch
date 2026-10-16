// Answer a pending Match_interesse (only the target student can accept or refuse)
query "match_interesse/{match_interesse_id}" verb=PATCH {
  api_group = "Authentication"
  auth = "user"

  input {
    int match_interesse_id? filters=min:1
    enum status {
      values = ["match", "recusado"]
    }
  }

  stack {
    db.get Match_interesse {
      field_name = "id"
      field_value = $input.match_interesse_id
    } as $atual
  
    precondition ($atual != null) {
      error_type = "notfound"
      error = "Interesse de match não encontrado."
    }
  
    precondition ($atual.usuario_alvo_id == $auth.id) {
      error_type = "accessdenied"
      error = "Só o aluno que recebeu o interesse pode respondê-lo."
    }
  
    precondition ($atual.status == "pendente") {
      error_type = "inputerror"
      error = "Este interesse já foi respondido."
    }
  
    db.patch Match_interesse {
      field_name = "id"
      field_value = $input.match_interesse_id
      data = {status: $input.status}
    } as $match_interesse
  }

  response = $match_interesse
  guid = "2w7RDvF_lelZQbfBG2y9h0kpJmU"
}