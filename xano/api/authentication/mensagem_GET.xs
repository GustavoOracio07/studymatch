// Messages of a confirmed match, oldest first: the last 50, or the first 50 after the id "depois_de"
query mensagem verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
    int match_interesse_id
    int depois_de?
  }

  stack {
    function.run "StudyMatch/exigir_conversa" {
      input = {
        user_id           : $auth.id
        match_interesse_id: $input.match_interesse_id
      }
    } as $match
  
    var $encontradas {
      value = []
    }
  
    conditional {
      if ($input.depois_de > 0) {
        db.query mensagem {
          where = $db.mensagem.match_interesse_id == $match.id && $db.mensagem.id > $input.depois_de
          sort = {mensagem.id: "asc"}
          return = {type: "list", paging: {page: 1, per_page: 50}}
        } as $novas
      
        var.update $encontradas {
          value = $novas.items
        }
      }
    
      else {
        db.query mensagem {
          where = $db.mensagem.match_interesse_id == $match.id
          sort = {mensagem.id: "desc"}
          return = {type: "list", paging: {page: 1, per_page: 50}}
        } as $ultimas
      
        var.update $encontradas {
          value = $ultimas.items|reverse
        }
      }
    }
  
    var $mensagens {
      value = []
    }
  
    foreach ($encontradas) {
      each as $m {
        var.update $mensagens {
          value = $mensagens
            |push:```
              {
                id          : $m.id
                remetente_id: $m.remetente_id
                texto       : $m.texto
                created_at  : $m.created_at
              }
              ```
        }
      }
    }
  }

  response = $mensagens
  guid = "-78leRe0tWtKUH0k99ffalOcq7k"
}