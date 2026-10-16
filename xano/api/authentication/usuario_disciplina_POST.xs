// Add a Usuario_disciplina record for the authenticated user
query usuario_disciplina verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
    int disciplina_id {
      table = "Disciplina"
    }
  }

  stack {
    function.run "StudyMatch/validar_disciplina_do_curso" {
      input = {user_id: $auth.id, disciplina_id: $input.disciplina_id}
    }
  
    db.query Usuario_disciplina {
      where = $db.Usuario_disciplina.usuario_id == $auth.id && $db.Usuario_disciplina.disciplina_id == $input.disciplina_id
      return = {type: "exists"}
    } as $repetida
  
    precondition ($repetida == false) {
      error_type = "inputerror"
      error = "Esta disciplina já está na sua lista."
    }
  
    // The owner is always the authenticated user
    db.add Usuario_disciplina {
      data = {
        created_at   : "now"
        usuario_id   : $auth.id
        disciplina_id: $input.disciplina_id
      }
    } as $usuario_disciplina
  }

  response = $usuario_disciplina
  guid = "dTVnd9jiXkaIN80vTdZ6Wg5_9B0"
}