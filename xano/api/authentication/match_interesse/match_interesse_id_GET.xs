// Get a Match_interesse record where the authenticated user is origin or target
query "match_interesse/{match_interesse_id}" verb=GET {
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
  
    precondition ($match_interesse.usuario_id == $auth.id || $match_interesse.usuario_alvo_id == $auth.id) {
      error_type = "accessdenied"
      error = "Você só pode acessar interesses em que participa."
    }
  }

  response = $match_interesse
  guid = "6HUQxwdQjX2ezqxA92S3mTRjXRk"
}