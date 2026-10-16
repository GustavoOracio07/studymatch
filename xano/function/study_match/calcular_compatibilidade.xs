// Compatibilidade entre dois alunos: 60% disciplinas de dificuldade em comum + 40% minutos de disponibilidade em comum.
// Cada parte = em comum / menor dos dois conjuntos (coeficiente de sobreposição), o que torna o cálculo simétrico.
function "StudyMatch/calcular_compatibilidade" {
  input {
    int usuario_a
    int usuario_b
  }

  stack {
    // --- Disciplinas
    db.query Usuario_disciplina {
      where = $db.Usuario_disciplina.usuario_id == $input.usuario_a
      return = {type: "list"}
    } as $disciplinas_a
  
    db.query Usuario_disciplina {
      where = $db.Usuario_disciplina.usuario_id == $input.usuario_b
      return = {type: "list"}
    } as $disciplinas_b
  
    var $ids_a {
      value = $disciplinas_a|map:$$.disciplina_id
    }
  
    var $ids_b {
      value = $disciplinas_b|map:$$.disciplina_id
    }
  
    var $disciplinas_comuns {
      value = $ids_a|intersect:$ids_b
    }
  
    var $menor_disciplinas {
      value = ($ids_a|count)|min:($ids_b|count)
    }
  
    var $nota_disciplinas {
      value = 0
    }
  
    conditional {
      if ($menor_disciplinas > 0) {
        var.update $nota_disciplinas {
          value = (($disciplinas_comuns|count)|to_decimal) / $menor_disciplinas
        }
      }
    }
  
    // --- Horários
    db.query Disponibilidade {
      where = $db.Disponibilidade.usuario_id == $input.usuario_a
      return = {type: "list"}
    } as $faixas_a
  
    db.query Disponibilidade {
      where = $db.Disponibilidade.usuario_id == $input.usuario_b
      return = {type: "list"}
    } as $faixas_b
  
    var $total_a {
      value = 0
    }
  
    foreach ($faixas_a) {
      each as $faixa {
        var.update $total_a {
          value = $total_a + ((($faixa.hora_fim|substr:0:2|to_int) * 60) + ($faixa.hora_fim|substr:3:2|to_int)) - ((($faixa.hora_inicio|substr:0:2|to_int) * 60) + ($faixa.hora_inicio|substr:3:2|to_int))
        }
      }
    }
  
    var $total_b {
      value = 0
    }
  
    foreach ($faixas_b) {
      each as $faixa {
        var.update $total_b {
          value = $total_b + ((($faixa.hora_fim|substr:0:2|to_int) * 60) + ($faixa.hora_fim|substr:3:2|to_int)) - ((($faixa.hora_inicio|substr:0:2|to_int) * 60) + ($faixa.hora_inicio|substr:3:2|to_int))
        }
      }
    }
  
    var $minutos_comuns {
      value = 0
    }
  
    var $horarios_comuns {
      value = []
    }
  
    foreach ($faixas_a) {
      each as $fa {
        foreach ($faixas_b) {
          each as $fb {
            conditional {
              if ($fa.dia_semana == $fb.dia_semana && $fa.hora_inicio < $fb.hora_fim && $fb.hora_inicio < $fa.hora_fim) {
                var $inicio_comum {
                  value = $fa.hora_inicio
                }
              
                conditional {
                  if ($fb.hora_inicio > $fa.hora_inicio) {
                    var.update $inicio_comum {
                      value = $fb.hora_inicio
                    }
                  }
                }
              
                var $fim_comum {
                  value = $fa.hora_fim
                }
              
                conditional {
                  if ($fb.hora_fim < $fa.hora_fim) {
                    var.update $fim_comum {
                      value = $fb.hora_fim
                    }
                  }
                }
              
                var.update $minutos_comuns {
                  value = $minutos_comuns + ((($fim_comum|substr:0:2|to_int) * 60) + ($fim_comum|substr:3:2|to_int)) - ((($inicio_comum|substr:0:2|to_int) * 60) + ($inicio_comum|substr:3:2|to_int))
                }
              
                var.update $horarios_comuns {
                  value = $horarios_comuns
                    |push:{dia_semana: $fa.dia_semana, hora_inicio: $inicio_comum, hora_fim: $fim_comum}
                }
              }
            }
          }
        }
      }
    }
  
    var $menor_total {
      value = $total_a|min:$total_b
    }
  
    var $nota_horarios {
      value = 0
    }
  
    conditional {
      if ($menor_total > 0) {
        var.update $nota_horarios {
          value = ($minutos_comuns|to_decimal) / $menor_total
        }
      }
    }
  
    var $percentual {
      value = ((60 * $nota_disciplinas) + (40 * $nota_horarios))|round|to_int
    }
  }

  response = {
    percentual        : $percentual
    disciplinas_comuns: $disciplinas_comuns
    horarios_comuns   : $horarios_comuns
  }

  guid = "WGieLhwS3uR8Cx1apebjcSwV8mM"
}