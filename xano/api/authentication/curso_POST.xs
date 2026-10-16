// Add curso record
query curso verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
    dblink {
      table = "curso"
    }
  }

  stack {
    // Courses and subjects are maintained only through the Xano panel (admin role)
    function.run "StudyMatch/exigir_admin" {
      input = {user_id: $auth.id}
    }
  
    db.add curso {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $curso
  }

  response = $curso
  guid = "3WyWDS79JzDTfXqFE3rMR6jP_Gk"
}