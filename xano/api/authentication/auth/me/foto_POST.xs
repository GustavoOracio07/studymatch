// Envia ou troca a foto de perfil do usuário autenticado (multipart, campo "foto")
query "auth/me/foto" verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
    file? foto
  }

  stack {
    precondition ($input.foto != null) {
      error_type = "inputerror"
      error = "Envie uma foto."
    }
  
    var $nova {
      value = null
    }
  
    // create_image é o único upload disponível no plano free (create_attachment é bloqueado).
    // Ele recusa o que não é imagem com erro 500; a recusa vira um erro de validação
    try_catch {
      try {
        storage.create_image {
          value = $input.foto
          access = "public"
          filename = $input.foto.name
        } as $imagem
      
        var.update $nova {
          value = $imagem
        }
      }
    
      catch {
        var.update $nova {
          value = null
        }
      }
    }
  
    precondition ($nova != null) {
      error_type = "inputerror"
      error = "Envie uma imagem JPEG, PNG ou WEBP."
    }
  
    // Confere o tipo e o tamanho medidos pelo Xano; se a foto for inválida, apaga o arquivo
    conditional {
      if ((["image/jpeg", "image/png", "image/webp"]|in:$nova.mime) == false) {
        storage.delete_file {
          pathname = $nova.path
        }
      
        precondition (false) {
          error_type = "inputerror"
          error = "Envie uma imagem JPEG, PNG ou WEBP."
        }
      }
    
      elseif ($nova.size > 2097152) {
        storage.delete_file {
          pathname = $nova.path
        }
      
        precondition (false) {
          error_type = "inputerror"
          error = "A foto deve ter no máximo 2 MB."
        }
      }
    }
  
    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "Foto"]
    } as $atual
  
    db.edit user {
      field_name = "id"
      field_value = $auth.id
      data = {Foto: $nova}
    } as $editado
  
    // A foto anterior só é apagada depois que a nova foi gravada
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
      ]
    } as $user
  
    function.run "StudyMatch/url_foto" {
      input = {foto: $user.Foto}
    } as $foto_url
  }

  response = $user
    |unset:"Foto"
    |set:"foto_url":$foto_url
  guid = "aVnTmqmCwF9QSmGjUhy9bRtXXgo"
}