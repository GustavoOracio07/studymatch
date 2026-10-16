// Interests received, sent and confirmed for the authenticated user.
// The other student's phone is only included for confirmed matches.
query meus_matches verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    db.query Match_interesse {
      where = $db.Match_interesse.usuario_id == $auth.id || $db.Match_interesse.usuario_alvo_id == $auth.id
      sort = {Match_interesse.created_at: "desc"}
      return = {type: "list"}
    } as $interesses
  
    var $recebidos {
      value = []
    }
  
    var $enviados {
      value = []
    }
  
    var $confirmados {
      value = []
    }
  
    foreach ($interesses) {
      each as $interesse {
        var $colega_id {
          value = $interesse.usuario_id
        }
      
        conditional {
          if ($interesse.usuario_id == $auth.id) {
            var.update $colega_id {
              value = $interesse.usuario_alvo_id
            }
          }
        }
      
        db.get user {
          field_name = "id"
          field_value = $colega_id
          output = ["id", "Name", "Sobrenome", "Semestre", "Sobre_mim", "Telefone"]
        } as $colega
      
        // Records of students who deleted their account are ignored
        conditional {
          if ($colega != null) {
            var $item {
              value = {
                interesse_id: $interesse.id
                status      : $interesse.status
                percentual  : $interesse.percentual_compatibilidade
                usuario_id  : $colega.id
                nome        : $colega.Name
                sobrenome   : $colega.Sobrenome
                semestre    : $colega.Semestre
                sobre_mim   : $colega.Sobre_mim
              }
            }
          
            conditional {
              if ($interesse.status == "match") {
                var.update $confirmados {
                  value = $confirmados
                    |push:($item|set:"telefone":$colega.Telefone)
                }
              }
            
              elseif ($interesse.status == "pendente" && $interesse.usuario_alvo_id == $auth.id) {
                var.update $recebidos {
                  value = $recebidos|push:$item
                }
              }
            
              elseif ($interesse.usuario_id == $auth.id) {
                var.update $enviados {
                  value = $enviados|push:$item
                }
              }
            }
          }
        }
      }
    }
  }

  response = {
    recebidos  : $recebidos
    enviados   : $enviados
    confirmados: $confirmados
  }

  guid = "TwunVyvBc1kIXpzq24cLvZuC7No"
}