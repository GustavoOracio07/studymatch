// Mensagens da conversa entre os dois alunos de um match confirmado
table mensagem {
  auth = false

  schema {
    int id
    timestamp created_at?=now
    int match_interesse_id? {
      table = "Match_interesse"
    }
  
    int remetente_id? {
      table = "user"
    }
  
    // Guardado para apagar as mensagens recebidas quando o aluno exclui a conta
    int destinatario_id? {
      table = "user"
    }
  
    text texto? filters=trim
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {
      type : "btree"
      field: [
        {name: "match_interesse_id", op: "asc"}
        {name: "id", op: "desc"}
      ]
    }
  ]

  guid = "BQjLaP6wTCf2OIULvH6sp03cYYA"
}