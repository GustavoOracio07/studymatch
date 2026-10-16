// Apaga um usuário e, em cascata, as disponibilidades, as disciplinas de dificuldade e os interesses de match dele
function "StudyMatch/excluir_usuario" {
  input {
    int user_id
  }

  stack {
    db.transaction {
      stack {
        db.bulk.delete Disponibilidade {
          where = $db.Disponibilidade.usuario_id == $input.user_id
        } as $disponibilidades_apagadas
      
        db.bulk.delete Usuario_disciplina {
          where = $db.Usuario_disciplina.usuario_id == $input.user_id
        } as $disciplinas_apagadas
      
        // Interesses de match em que o usuário é origem ou alvo (qualquer status)
        db.bulk.delete Match_interesse {
          where = $db.Match_interesse.usuario_id == $input.user_id || $db.Match_interesse.usuario_alvo_id == $input.user_id
        } as $matches_apagados
      
        db.del user {
          field_name = "id"
          field_value = $input.user_id
        }
      }
    }
  }

  response = null
  guid = "B96FXd4EqFBoV72LaEMTIWfp80c"
}