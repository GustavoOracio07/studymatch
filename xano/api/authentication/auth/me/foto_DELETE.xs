// Remove a foto de perfil do usuário autenticado (sem foto, não faz nada)
query "auth/me/foto" verb=DELETE {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "Foto", "Foto_dados"]
    } as $atual

    conditional {
      if ($atual.Foto != null || $atual.Foto_dados != null) {
        db.edit user {
          field_name = "id"
          field_value = $auth.id
          data = {Foto: null, Foto_dados: null}
        } as $editado

        // Foto antiga no armazenamento: apaga também o arquivo
        conditional {
          if ($atual.Foto != null && $atual.Foto.path != null) {
            storage.delete_file {
              pathname = $atual.Foto.path
            }
          }
        }
      }
    }
  }

  response = null
  guid = "wsSdqGNOT8oAVwbYOkqslQijka0"
}