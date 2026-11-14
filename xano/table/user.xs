// Stores user information and allows the user to authenticate  against
table user {
  auth = true

  schema {
    int id
    timestamp created_at?=now
    text Name filters=trim
    email? email filters=trim|lower
    password? Password filters=min:8|minAlpha:1|minDigit:1
  
    // The role of the user within their company (e.g., 'admin', 'member').
    enum role? {
      values = ["admin", "member"]
    }
  
    object password_reset? {
      schema {
        password token?
        timestamp? expiration?
        bool used?
      }
    }
  
    text Sobrenome? filters=trim
    int curso_id? {
      table = "curso"
    }
  
    int Semestre?
    text Telefone? filters=trim
    text Sobre_mim? filters=trim
  
    // Foto de perfil antiga (arquivo no armazenamento do Xano, que no plano free leva marca d'água).
    // Só é lida enquanto o aluno não envia uma foto nova; os envios novos vão para Foto_dados.
    image? Foto?

    // Foto de perfil como data URL JPEG (data:image/jpeg;base64,...), já reduzida pelo frontend
    text? Foto_dados?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {
      type : "btree|unique"
      field: [{name: "Telefone", op: "asc"}]
    }
  ]

  tags = ["xano:quick-start"]
  guid = "BsBqYbtS_wQLfNUKWQaP3Uiin8w"
}