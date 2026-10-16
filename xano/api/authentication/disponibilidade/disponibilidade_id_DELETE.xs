// Delete a Disponibilidade record owned by the authenticated user
query "disponibilidade/{disponibilidade_id}" verb=DELETE {
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
      error = "Você só pode apagar as suas próprias disponibilidades."
    }
  
    db.del Disponibilidade {
      field_name = "id"
      field_value = $input.disponibilidade_id
    }
  }

  response = null
  guid = "Q21zGNm69privGUMZK_Fs121AXk"
}