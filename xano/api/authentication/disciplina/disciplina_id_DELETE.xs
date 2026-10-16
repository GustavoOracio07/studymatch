// Delete Disciplina record.
query "disciplina/{disciplina_id}" verb=DELETE {
  api_group = "Authentication"
  auth = "user"

  input {
    int disciplina_id? filters=min:1
  }

  stack {
    // Courses and subjects are maintained only through the Xano panel (admin role)
    function.run "StudyMatch/exigir_admin" {
      input = {user_id: $auth.id}
    }
  
    db.del Disciplina {
      field_name = "id"
      field_value = $input.disciplina_id
    }
  }

  response = null
  guid = "PCAW95qD3g4XmKyBxXU7UsqDXBA"
}