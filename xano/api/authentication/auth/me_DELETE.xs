// Delete the account of the authenticated user, with cascade
query "auth/me" verb=DELETE {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    function.run "StudyMatch/excluir_usuario" {
      input = {user_id: $auth.id}
    }
  }

  response = null
  guid = "np-sk-ORzbk2abB9K6eIHDVPxgw"
}