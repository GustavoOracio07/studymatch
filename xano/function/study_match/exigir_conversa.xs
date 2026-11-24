// Garante que o aluno participa de um match confirmado e devolve o registro do match
function "StudyMatch/exigir_conversa" {
  input {
    int user_id
    int match_interesse_id
  }

  stack {
    db.get Match_interesse {
      field_name = "id"
      field_value = $input.match_interesse_id
    } as $match
  
    precondition ($match != null) {
      error_type = "notfound"
      error = "Match não encontrado."
    }
  
    precondition ($match.usuario_id == $input.user_id || $match.usuario_alvo_id == $input.user_id) {
      error_type = "accessdenied"
      error = "Você só pode acessar conversas dos seus matches."
    }
  
    precondition ($match.status == "match") {
      error_type = "accessdenied"
      error = "A conversa só é liberada depois do match confirmado."
    }
  }

  response = $match
  guid = "NepymLWXer87DFvx_Fmxr3M3dQQ"
}