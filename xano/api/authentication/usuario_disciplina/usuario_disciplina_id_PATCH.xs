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
  
    function.run "StudyMatch/validar_disciplina_do_curso" {
      input = {user_id: $auth.id, disciplina_id: $input.disciplina_id}
    }
  
    db.query Usuario_disciplina {
      where = $db.Usuario_disciplina.usuario_id == $auth.id && $db.Usuario_disciplina.disciplina_id == $input.disciplina_id && $db.Usuario_disciplina.id != $atual.id
      return = {type: "exists"}
    } as $repetida
  
    precondition ($repetida == false) {
      error_type = "inputerror"
      error = "Esta disciplina já está na sua lista."
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