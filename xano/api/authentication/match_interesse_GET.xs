// Query the Match_interesse records where the authenticated user is origin or target
query match_interesse verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    db.query Match_interesse {
      where = $db.Match_interesse.usuario_id == $auth.id || $db.Match_interesse.usuario_alvo_id == $auth.id
      return = {type: "list"}
    } as $match_interesse
  }

  response = $match_interesse
  guid = "vdXrdz_NfMoexTsJ3qTFkWGVoUI"
}