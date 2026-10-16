// Edit Disciplina record
query "disciplina/{disciplina_id}" verb=PATCH {
  api_group = "Authentication"
  auth = "user"

  input {
    int disciplina_id? filters=min:1
    dblink {
      table = "Disciplina"
    }
  }

  stack {
    // Courses and subjects are maintained only through the Xano panel (admin role)
    function.run "StudyMatch/exigir_admin" {
      input = {user_id: $auth.id}
    }
  
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch Disciplina {
      field_name = "id"
      field_value = $input.disciplina_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $disciplina
  }

  response = $disciplina
  guid = "6yhuy59UWp2xYpOgkl5y6BoGQss"
}