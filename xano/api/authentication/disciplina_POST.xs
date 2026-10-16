// Add Disciplina record
query disciplina verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
    dblink {
      table = "Disciplina"
    }
  }

  stack {
    // Courses and subjects are maintained only through the Xano panel (admin role)
    function.run "StudyMatch/exigir_admin" {
      input = {user_id: $auth.id}
    }
  
    db.add Disciplina {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $disciplina
  }

  response = $disciplina
  guid = "Nb65ZEjjlawXynv9OQspd9D_MK4"
}