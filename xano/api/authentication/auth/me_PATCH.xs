// Edit the profile of the authenticated user (the client always sends the full profile)
query "auth/me" verb=PATCH {
  api_group = "Authentication"
  auth = "user"

  input {
    text name filters=trim
    text sobrenome filters=trim
    text telefone filters=trim
    int curso_id
    int semestre
    text? sobre_mim? filters=trim
  }

  stack {
    precondition ($input.name != "" && $input.sobrenome != "" && $input.telefone != "") {
      error_type = "inputerror"
      error = "Preencha nome, sobrenome e telefone."
    }
  
    precondition ($input.semestre >= 1 && $input.semestre <= 12) {
      error_type = "inputerror"
      error = "O semestre deve estar entre 1 e 12"
    }
  
    db.has curso {
      field_name = "id"
      field_value = $input.curso_id
    } as $curso_existe
  
    precondition ($curso_existe) {
      error_type = "inputerror"
      error = "Curso não encontrado."
    }
  
    db.query user {
      where = $db.user.Telefone == $input.telefone && $db.user.id != $auth.id
      return = {type: "exists"}
    } as $telefone_em_uso
  
    precondition ($telefone_em_uso == false) {
      error_type = "inputerror"
      error = "Este telefone já está cadastrado."
    }
  
    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "curso_id"]
    } as $atual
  
    db.transaction {
      stack {
        // Subjects belong to a course: changing course removes the old ones
        conditional {
          if ($atual.curso_id != $input.curso_id) {
            db.bulk.delete Usuario_disciplina {
              where = $db.Usuario_disciplina.usuario_id == $auth.id
            } as $disciplinas_removidas
          }
        }
      
        db.edit user {
          field_name = "id"
          field_value = $auth.id
          data = {
            Name     : $input.name
            Sobrenome: $input.sobrenome
            Telefone : $input.telefone
            curso_id : $input.curso_id
            Semestre : $input.semestre
            Sobre_mim: $input.sobre_mim
          }
        } as $editado
      }
    }
  
    // Read the profile again with explicit fields so the password hash is never returned
    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = [
        "id"
        "created_at"
        "Name"
        "Sobrenome"
        "email"
        "role"
        "curso_id"
        "Semestre"
        "Telefone"
        "Sobre_mim"
      ]
    } as $user
  }

  response = $user
  guid = "PA43xyCa95HewNte8EF1CP5BvnI"
}