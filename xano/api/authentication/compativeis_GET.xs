// List the students compatible with the authenticated user (at least one difficulty subject in common), best match first.
// Never returns phone or e-mail.
query compativeis verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "curso_id"]
    } as $aluno
  
    // Subjects belong to a course, so only students of the same course can share one
    db.query user {
      where = $db.user.curso_id == $aluno.curso_id && $db.user.id != $auth.id
      return = {type: "list"}
      output = ["id", "Name", "Sobrenome", "Semestre", "Sobre_mim"]
    } as $colegas
  
    db.query Match_interesse {
      where = $db.Match_interesse.usuario_id == $auth.id || $db.Match_interesse.usuario_alvo_id == $auth.id
      return = {type: "list"}
    } as $interesses
  
    var $compativeis {
      value = []
    }
  
    foreach ($colegas) {
      each as $colega {
        function.run "StudyMatch/calcular_compatibilidade" {
          input = {usuario_a: $auth.id, usuario_b: $colega.id}
        } as $compatibilidade
      
        conditional {
          if (($compatibilidade.disciplinas_comuns|count) > 0) {
            // Interest status between the two, by priority: match > recebido > enviado > recusado
            var $situacao {
              value = "nenhum"
            }
          
            var $interesse_id {
              value = null
            }
          
            var $prioridade {
              value = 0
            }
          
            foreach ($interesses) {
              each as $interesse {
                var $situacao_deste {
                  value = null
                }
              
                var $prioridade_deste {
                  value = 0
                }
              
                conditional {
                  if ($interesse.status == "match" && ($interesse.usuario_id == $colega.id || $interesse.usuario_alvo_id == $colega.id)) {
                    var.update $situacao_deste {
                      value = "match"
                    }
                  
                    var.update $prioridade_deste {
                      value = 4
                    }
                  }
                
                  elseif ($interesse.status == "pendente" && $interesse.usuario_id == $colega.id) {
                    var.update $situacao_deste {
                      value = "recebido"
                    }
                  
                    var.update $prioridade_deste {
                      value = 3
                    }
                  }
                
                  elseif ($interesse.status == "pendente" && $interesse.usuario_alvo_id == $colega.id) {
                    var.update $situacao_deste {
                      value = "enviado"
                    }
                  
                    var.update $prioridade_deste {
                      value = 2
                    }
                  }
                
                  elseif ($interesse.status == "recusado" && ($interesse.usuario_id == $colega.id || $interesse.usuario_alvo_id == $colega.id)) {
                    var.update $situacao_deste {
                      value = "recusado"
                    }
                  
                    var.update $prioridade_deste {
                      value = 1
                    }
                  }
                }
              
                conditional {
                  if ($prioridade_deste > $prioridade) {
                    var.update $prioridade {
                      value = $prioridade_deste
                    }
                  
                    var.update $situacao {
                      value = $situacao_deste
                    }
                  
                    var.update $interesse_id {
                      value = $interesse.id
                    }
                  }
                }
              }
            }
          
            var.update $compativeis {
              value = $compativeis
                |push:```
                  {
                    usuario_id        : $colega.id
                    nome              : $colega.Name
                    sobrenome         : $colega.Sobrenome
                    semestre          : $colega.Semestre
                    sobre_mim         : $colega.Sobre_mim
                    percentual        : $compatibilidade.percentual
                    disciplinas_comuns: $compatibilidade.disciplinas_comuns
                    horarios_comuns   : $compatibilidade.horarios_comuns
                    situacao          : $situacao
                    interesse_id      : $interesse_id
                  }
                  ```
            }
          }
        }
      }
    }
  }

  response = $compativeis|sort:"percentual":"number":false
  guid = "DRtg9erilGeEsn_6S-4js32RVfM"
}