// Garante que a disciplina existe e pertence ao curso do aluno
function "StudyMatch/validar_disciplina_do_curso" {
  input {
    int user_id
    int disciplina_id
  }

  stack {
    db.get user {
      field_name = "id"
      field_value = $input.user_id
      output = ["id", "curso_id"]
    } as $aluno
  
    db.get Disciplina {
      field_name = "id"
      field_value = $input.disciplina_id
    } as $disciplina
  
    precondition ($disciplina != null && $aluno != null && $disciplina.curso_id == $aluno.curso_id) {
      error_type = "inputerror"
      error = "Escolha apenas disciplinas do seu curso."
    }
  }

  response = null
  guid = "rwNK1NyyCD_YQ5tzB545N0AfZR4"
}