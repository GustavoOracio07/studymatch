// Apaga um usuário e, em cascata, as disponibilidades, as disciplinas de dificuldade, os interesses de match, as mensagens e a foto dele
function "StudyMatch/excluir_usuario" {
  input {
    int user_id
  }

  stack {
    db.get user {
      field_name = "id"
      field_value = $input.user_id
      output = ["id", "Foto"]
    } as $aluno
  
    db.transaction {
      stack {
        db.bulk.delete Disponibilidade {
          where = $db.Disponibilidade.usuario_id == $input.user_id
        } as $disponibilidades_apagadas
      
        db.bulk.delete Usuario_disciplina {
          where = $db.Usuario_disciplina.usuario_id == $input.user_id
        } as $disciplinas_apagadas
      
        // Mensagens enviadas e recebidas nas conversas do usuário
        db.bulk.delete mensagem {
          where = $db.mensagem.remetente_id == $input.user_id || $db.mensagem.destinatario_id == $input.user_id
        } as $mensagens_apagadas
      
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
  
    // O arquivo da foto fica fora do banco; é apagado depois que a conta foi removida
    conditional {
      if ($aluno.Foto != null && $aluno.Foto.path != null) {
        storage.delete_file {
          pathname = $aluno.Foto.path
        }
      }
    }
  }

  response = null
  guid = "B96FXd4EqFBoV72LaEMTIWfp80c"
}