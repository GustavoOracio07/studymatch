// Delete curso record.
query "curso/{curso_id}" verb=DELETE {
  api_group = "Authentication"
  auth = "user"

  input {
    int curso_id? filters=min:1
  }

  stack {
    // Courses and subjects are maintained only through the Xano panel (admin role)
    function.run "StudyMatch/exigir_admin" {
      input = {user_id: $auth.id}
    }
  
    db.del curso {
      field_name = "id"
      field_value = $input.curso_id
    }
  }

  response = null
  guid = "d4rzL169YP0ce6ysj76pR59RSEs"
}