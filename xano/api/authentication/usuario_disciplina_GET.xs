// Query the Usuario_disciplina records of the authenticated user
query usuario_disciplina verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    db.query Usuario_disciplina {
      where = $db.Usuario_disciplina.usuario_id == $auth.id
      return = {type: "list"}
    } as $usuario_disciplina
  }

  response = $usuario_disciplina
  guid = "a_e-R3FFUujx2-ErbVWftS0CRNE"
}