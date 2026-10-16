// Show interest in another student. The compatibility is calculated by the backend.
// If the other student already sent a pending interest, that record becomes a match (cross interest).
query match_interesse verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
    int usuario_alvo_id
  }

  stack {
    precondition ($input.usuario_alvo_id != $auth.id) {
      error_type = "inputerror"
      error = "Você não pode dar match em si mesmo"
    }
  
    db.has user {
      field_name = "id"
      field_value = $input.usuario_alvo_id
    } as $alvo_existe
  
    precondition ($alvo_existe) {
      error_type = "notfound"
      error = "Aluno não encontrado."
    }
  
    db.query Match_interesse {
      where = $db.Match_interesse.usuario_id == $input.usuario_alvo_id && $db.Match_interesse.usuario_alvo_id == $auth.id
      return = {type: "single"}
    } as $inverso
  
    db.query Match_interesse {
      where = $db.Match_interesse.usuario_id == $auth.id && $db.Match_interesse.usuario_alvo_id == $input.usuario_alvo_id
      return = {type: "single"}
    } as $existente
  
    precondition (($inverso == null || $inverso.status != "match") && ($existente == null || $existente.status != "match")) {
      error_type = "inputerror"
      error = "Vocês já têm um match."
    }
  
    var $resultado {
      value = null
    }
  
    conditional {
      if ($inverso != null && $inverso.status == "pendente") {
        // Cross interest: accept the existing record instead of creating a new one
        db.edit Match_interesse {
          field_name = "id"
          field_value = $inverso.id
          data = {status: "match"}
        } as $aceito
      
        var.update $resultado {
          value = $aceito
        }
      }
    
      else {
        precondition ($existente == null) {
          error_type = "inputerror"
          error = "Você já demonstrou interesse neste colega."
        }
      
        function.run "StudyMatch/calcular_compatibilidade" {
          input = {usuario_a: $auth.id, usuario_b: $input.usuario_alvo_id}
        } as $compatibilidade
      
        // The origin is always the authenticated user and every new interest starts as pending
        db.add Match_interesse {
          data = {
            created_at                : "now"
            usuario_id                : $auth.id
            usuario_alvo_id           : $input.usuario_alvo_id
            percentual_compatibilidade: $compatibilidade.percentual
            status                    : "pendente"
          }
        } as $novo
      
        var.update $resultado {
          value = $novo
        }
      }
    }
  }

  response = $resultado
  guid = "aSaiU-kVZ34qwzRZTlqXdi3s9hE"
}