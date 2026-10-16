// Replace the whole list of difficulty subjects of the authenticated user (only subjects of the student's course)
query minhas_disciplinas verb=PUT {
  api_group = "Authentication"
  auth = "user"

  input {
    int[] disciplina_ids
  }

  stack {
    var $ids {
      value = $input.disciplina_ids|unique
    }
  
    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "curso_id"]
    } as $aluno
  
    db.query Disciplina {
      where = $db.Disciplina.curso_id == $aluno.curso_id
      return = {type: "list"}
    } as $disciplinas_do_curso
  
    var $invalidas {
      value = $ids
        |diff:($disciplinas_do_curso|map:$$.id)
    }
  
    precondition (($invalidas|count) == 0) {
      error_type = "inputerror"
      error = "Escolha apenas disciplinas do seu curso."
    }
  
    db.transaction {
      stack {
        db.bulk.delete Usuario_disciplina {
          where = $db.Usuario_disciplina.usuario_id == $auth.id
        } as $removidas
      
        foreach ($ids) {
          each as $disciplina_id {
            db.add Usuario_disciplina {
              data = {
                created_at   : "now"
                usuario_id   : $auth.id
                disciplina_id: $disciplina_id
              }
            } as $nova
          }
        }
      }
    }
  
    db.query Usuario_disciplina {
      where = $db.Usuario_disciplina.usuario_id == $auth.id
      return = {type: "list"}
    } as $minhas
  }

  response = $minhas
  guid = "u4wTAEFXv_1vKucmAwQKldHN39k"
}