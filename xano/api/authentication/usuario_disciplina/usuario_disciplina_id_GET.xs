// Get a Usuario_disciplina record owned by the authenticated user
query "usuario_disciplina/{usuario_disciplina_id}" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
    int usuario_disciplina_id? filters=min:1
  }

  stack {
    db.get Usuario_disciplina {
      field_name = "id"
      field_value = $input.usuario_disciplina_id
    } as $usuario_disciplina
  
    precondition ($usuario_disciplina != null) {
      error_type = "notfound"
      error = "Disciplina de dificuldade não encontrada."
    }
  
    precondition ($usuario_disciplina.usuario_id == $auth.id) {
      error_type = "accessdenied"
      error = "Você só pode acessar as suas próprias disciplinas de dificuldade."
    }
  }

  response = $usuario_disciplina
  guid = "S6VnydK2V1eDNEsJSZ0fdAC6OvI"
}