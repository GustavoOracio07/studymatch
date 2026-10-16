// Garante que o usuário tem papel admin (responde 403 caso contrário)
function "StudyMatch/exigir_admin" {
  input {
    int user_id
  }

  stack {
    db.get user {
      field_name = "id"
      field_value = $input.user_id
      output = ["id", "role"]
    } as $user
  
    precondition ($user != null && $user.role == "admin") {
      error_type = "accessdenied"
      error = "Cursos e disciplinas só podem ser alterados pelo painel do Xano."
    }
  }

  response = null
  guid = "bt-EC-N0Cql2Ajm0m1jxWnAqTf0"
}