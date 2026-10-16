// Apaga um usuário e, em cascata, as disponibilidades e as disciplinas de dificuldade dele
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