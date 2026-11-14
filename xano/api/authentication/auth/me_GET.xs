// Get the user record belonging to the authentication token
query "auth/me" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    // Get the user record based on the auth ID
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
        "Foto"
        "Foto_dados"
      ]
    } as $user
  
    function.run "StudyMatch/url_foto" {
      input = {foto: $user.Foto, foto_dados: $user.Foto_dados}
    } as $foto_url
  
    // Create an event log for get user record
    function.run "Quick Start/log_event" {
      input = {
        user_id : $user.id
        action  : "get_auth_user"
        metadata: {}
      }
    } as $event_log
  }

  response = $user
    |unset:"Foto"
    |unset:"Foto_dados"
    |set:"foto_url":$foto_url
  tags = ["xano:quick-start"]
  guid = "zUyJWgp9QlQX4aqCo5rbXRiIHkU"
}