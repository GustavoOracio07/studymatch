# Design

## Context

O Streamlit 1.64 tem navegação nativa (`st.navigation` / `st.Page`). A API do Xano usa token Bearer com validade de 24 h e, no plano free, aceita 10 requisições a cada 20 s. O Streamlit roda o script inteiro a cada interação, então chamadas soltas na página se repetem a cada clique.

## Goals / Non-Goals

**Goals:**
- Um único ponto de acesso à API, reutilizado por todas as telas.
- Poucas chamadas por interação.

**Non-Goals:**
- Persistir o login entre abas ou após recarregar a página (o token fica em `st.session_state`).
- Testes de interface com navegador real.

## Decisions

1. **Pacote `studymatch/`** com `api.py` (classe `XanoAPI` + exceção `ErroAPI`) e `sessao.py` (entrar, sair, aluno atual). As telas ficam em `paginas/`. O nome não é `pages/`, para não ativar a navegação automática antiga do Streamlit, que conflita com `st.navigation`.
2. **Configuração da URL:** primeiro a variável de ambiente `XANO_API_URL` (usada no Render), depois `st.secrets["XANO_API_URL"]` (uso local). Sem nenhuma das duas, o app mostra um erro de configuração claro.
3. **Erros:** o Xano devolve `{"code", "message"}`. `ErroAPI` carrega o status e a `message`, e as telas mostram essa mensagem com `st.error`. O 401 com token limpa a sessão. O 429 vira uma mensagem amigável. Erros de rede viram "Não foi possível falar com o servidor".
4. **Cache:** `GET /curso` e `GET /disciplina` com `st.cache_data(ttl=600)`, porque os dados são públicos e mudam pouco. O `auth/me` é guardado na sessão logo após o login e só é recarregado quando o perfil muda.
5. **Validação na tela é só conveniência** (campos obrigatórios). As regras valem no Xano.

## Risks / Trade-offs

- [Token só na memória da sessão] → Recarregar a página pede login de novo. Aceitável para o MVP.
- [Limite de requisições] → Cache e sessão reduzem as chamadas; o 429 tem mensagem própria.

## Migration Plan

Sem migração: `app.py` é substituído. Para rodar localmente: `streamlit run app.py` com `.streamlit/secrets.toml` configurado.
