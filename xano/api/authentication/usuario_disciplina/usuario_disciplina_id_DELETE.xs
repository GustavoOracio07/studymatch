// Delete a Usuario_disciplina record owned by the authenticated user
query "usuario_disciplina/{usuario_disciplina_id}" verb=DELETE {
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
      error = "Você só pode apagar as suas próprias disciplinas de dificuldade."
    }
  
    db.del Usuario_disciplina {
      field_name = "id"
      field_value = $input.usuario_disciplina_id
    }
  }

  response = null
  guid = "gHwRqIrooBSWo2wETc2fpVwDARQ"
}