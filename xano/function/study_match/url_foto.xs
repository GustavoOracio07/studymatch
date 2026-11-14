// Monta a URL pública da foto de perfil a partir do path guardado no campo Foto (null sem foto)
function "StudyMatch/url_foto" {
  input {
    json? foto?
  }

  stack {
    var $url {
      value = null
    }
  
    conditional {
      if ($input.foto != null && $input.foto.path != null) {
        // Arquivos públicos ficam na origem da instância, sem o "/api:<grupo>" da URL da API
        var.update $url {
          value = ($env.$api_baseurl|split:"/api:"|first) ~ $input.foto.path
        }
      }
    }
  }

  response = $url
  guid = "gk0WlyGnaWDwE2kyuG-gnuyWzI4"
}