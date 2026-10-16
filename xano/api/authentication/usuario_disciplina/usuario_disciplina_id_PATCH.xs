// Edit a Usuario_disciplina record owned by the authenticated user
query "usuario_disciplina/{usuario_disciplina_id}" verb=PATCH {
  api_group = "Authentication"
  auth = "user"

  input {
    int usuario_disciplina_id? filters=min:1
    int disciplina_id {
      table = "Disciplina"
    }
  }

  stack {
    db.get Usuario_disciplina {
      field_name = "id"
      field_value = $input.usuario_disciplina_id
    } as $atual
  
    precondition ($atual != null) {
      error_type = "notfound"
      error = "Disciplina de dificuldade não encontrada."
    }
  
    precondition ($atual.usuario_id == $auth.id) {
      error_type = "accessdenied"
      error = "Você só pode alterar as suas próprias disciplinas de dificuldade."
    }
  
    // Only the subject can change; the owner never changes
    db.patch Usuario_disciplina {
      field_name = "id"
      field_value = $input.usuario_disciplina_id
      data = {disciplina_id: $input.disciplina_id}
    } as $usuario_disciplina
  }

  response = $usuario_disciplina
  guid = "zFgzkkKgn_r9VgNDdqrNCPp7-TM"
}