// Get a Disponibilidade record owned by the authenticated user
query "disponibilidade/{disponibilidade_id}" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
    int disponibilidade_id? filters=min:1
  }

  stack {
    db.get Disponibilidade {
      field_name = "id"
      field_value = $input.disponibilidade_id
    } as $disponibilidade
  
    precondition ($disponibilidade != null) {
      error_type = "notfound"
      error = "Disponibilidade não encontrada."
    }
  
    precondition ($disponibilidade.usuario_id == $auth.id) {
      error_type = "accessdenied"
      error = "Você só pode acessar as suas próprias disponibilidades."
    }
  }

  response = $disponibilidade
  guid = "xW7vMcBIdYmd1G5GV2vcyRVDwEA"
}