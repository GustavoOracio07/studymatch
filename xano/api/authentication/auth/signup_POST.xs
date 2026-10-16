// Signup and retrieve an authentication token
query "auth/signup" verb=POST {
  api_group = "Authentication"

  input {
    text name
    email email filters=trim|lower
    text password
    text sobrenome filters=trim
    int curso_id
    int semestre
    text telefone filters=trim
    text sobre_mim? filters=trim
  }

  stack {
    precondition ($input.semestre >= 1 && $input.semestre <= 12) {
      error_type = "inputerror"
      error = "O semestre deve estar entre 1 e 12"
    }
  
    // Verify that the email being used to sign up is unique
    db.has user {
      field_name = "email"
      field_value = $input.email
    } as $email_em_uso
  
    precondition ($email_em_uso == false) {
      error_type = "inputerror"
      error = "Este e-mail já está cadastrado."
    }
  
    // Verify that the phone being used to sign up is unique
    db.has user {
      field_name = "Telefone"
      field_value = $input.telefone
    } as $telefone_em_uso
  
    precondition ($telefone_em_uso == false) {
      error_type = "inputerror"
      error = "Este telefone já está cadastrado."
    }
  
    // Create a new user record
    db.add user {
      data = {
        created_at: "now"
        Name      : $input.name
        email     : $input.email
        Password  : $input.password
        role      : "member"
        Sobrenome : $input.sobrenome
        curso_id  : $input.curso_id
        Semestre  : $input.semestre
        Telefone  : $input.telefone
        Sobre_mim : $input.sobre_mim
      }
    } as $user
  
    // Create an authentiction token
    security.create_auth_token {
      table = "user"
      extras = {}
      expiration = 86400
      id = $user.id
    } as $authToken
  
    // Create an event log for signup (never log the password hash)
    function.run "Quick Start/log_event" {
      input = {
        user_id : $user.id
        action  : "signup"
        metadata: {email: $user.email}
      }
    } as $event_log
  }

  response = {authToken: $authToken, user_id: $user.id}
  tags = ["xano:quick-start"]
  guid = "pAF6cbeYY1pkQ1qQq5skctYVXuQ"
}