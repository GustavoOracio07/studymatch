// Query the Disponibilidade records of the authenticated user
query disponibilidade verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    db.query Disponibilidade {
      where = $db.Disponibilidade.usuario_id == $auth.id
      sort = {
        Disponibilidade.dia_semana : "asc"
        Disponibilidade.hora_inicio: "asc"
      }
    
      return = {type: "list"}
    } as $disponibilidade
  }

  response = $disponibilidade
  guid = "sGp5yFbWxTGoHDLzBW9HOnkJ2lQ"
}