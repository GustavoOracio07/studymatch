// Envia ou troca a foto de perfil do usuário autenticado.
// A foto chega como data URL JPEG (campo "foto") e fica gravada no próprio registro (Foto_dados):
// o armazenamento de imagens do plano free do Xano coloca marca d'água nas fotos
query "auth/me/foto" verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
    text? foto
  }

  stack {
    precondition ($input.foto != null && $input.foto != "") {
      error_type = "inputerror"
      error = "Envie uma foto."
    }

    // Confere o começo da data URL ("data:image/jpeg;base64," tem 23 caracteres)
    precondition (($input.foto|substr:0:23) == "data:image/jpeg;base64,") {
      error_type = "inputerror"
      error = "Envie uma imagem JPEG, PNG ou WEBP."
    }

    // ~300 mil caracteres de base64 = ~220 KB de imagem (a foto reduzida a 256x256 tem bem menos)
    precondition (($input.foto|strlen) <= 300000) {
      error_type = "inputerror"
      error = "A foto é grande demais."
    }

    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "Foto"]
    } as $atual

    db.edit user {
      field_name = "id"
      field_value = $auth.id
      data = {Foto_dados: $input.foto, Foto: null}
    } as $editado

    // Se havia uma foto antiga no armazenamento, apaga o arquivo depois de gravar a nova
    conditional {
      if ($atual.Foto != null && $atual.Foto.path != null) {
        storage.delete_file {
          pathname = $atual.Foto.path
        }
      }
    }

    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = [
        "id"
        "created_at"
        "Name"
        "Sobrenome"
        "email"
        "role"
        "curso_id"
        "Semestre"
        "Telefone"
        "Sobre_mim"
        "Foto"
        "Foto_dados"
      ]
    } as $user

    function.run "StudyMatch/url_foto" {
      input = {foto: $user.Foto, foto_dados: $user.Foto_dados}
    } as $foto_url
  }

  response = $user
    |unset:"Foto"
    |unset:"Foto_dados"
    |set:"foto_url":$foto_url
  guid = "aVnTmqmCwF9QSmGjUhy9bRtXXgo"
}