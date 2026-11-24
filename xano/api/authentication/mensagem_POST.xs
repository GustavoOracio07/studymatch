// Send a message in the conversation of a confirmed match
query mensagem verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
    int match_interesse_id
    text texto filters=trim
  }

  stack {
    function.run "StudyMatch/exigir_conversa" {
      input = {
        user_id           : $auth.id
        match_interesse_id: $input.match_interesse_id
      }
    } as $match
  
    precondition ($input.texto != "") {
      error_type = "inputerror"
      error = "Escreva uma mensagem."
    }
  
    precondition (($input.texto|strlen) <= 500) {
      error_type = "inputerror"
      error = "A mensagem pode ter no máximo 500 caracteres."
    }
  
    var $destinatario_id {
      value = $match.usuario_id
    }
  
    conditional {
      if ($match.usuario_id == $auth.id) {
        var.update $destinatario_id {
          value = $match.usuario_alvo_id
        }
      }
    }
  
    // The sender is always the authenticated user
    db.add mensagem {
      data = {
        created_at        : "now"
        match_interesse_id: $match.id
        remetente_id      : $auth.id
        destinatario_id   : $destinatario_id
        texto             : $input.texto
      }
    } as $mensagem
  }

  response = {
    id          : $mensagem.id
    remetente_id: $mensagem.remetente_id
    texto       : $mensagem.texto
    created_at  : $mensagem.created_at
  }

  guid = "5Wi8JcVm4MamEqpS31kR6SKY8u4"
}