// Devolve a foto de perfil para exibir (null sem foto): a data URL de Foto_dados ou, para fotos
// antigas, a URL pública do arquivo guardado no campo Foto
function "StudyMatch/url_foto" {
  input {
    json? foto?
    text? foto_dados?
  }

  stack {
    var $url {
      value = null
    }

    conditional {
      if ($input.foto_dados != null && $input.foto_dados != "") {
        var.update $url {
          value = $input.foto_dados
        }
      }

      elseif ($input.foto != null && $input.foto.path != null) {
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