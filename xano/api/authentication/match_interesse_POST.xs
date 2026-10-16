// Add a Match_interesse record from the authenticated user to another student
query match_interesse verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
    int usuario_alvo_id {
      table = "user"
    }
  
    int percentual_compatibilidade
  }

  stack {
    precondition ($input.usuario_alvo_id != $auth.id) {
      error_type = "inputerror"
      error = "Você não pode dar match em si mesmo"
    }
  
    precondition ($input.percentual_compatibilidade >= 0 && $input.percentual_compatibilidade <= 100) {
      error_type = "inputerror"
      error = "O percentual deve estar entre 0 e 100"
    }
  
    // The origin is always the authenticated user and every new interest starts as pending
    db.add Match_interesse {
      data = {
        created_at                : "now"
        usuario_id                : $auth.id
        usuario_alvo_id           : $input.usuario_alvo_id
        percentual_compatibilidade: $input.percentual_compatibilidade
        status                    : "pendente"
      }
    } as $match_interesse
  }

  response = $match_interesse
  guid = "aSaiU-kVZ34qwzRZTlqXdi3s9hE"
}