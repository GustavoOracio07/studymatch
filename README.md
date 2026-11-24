# StudyMatch

Manual do usuário. A parte técnica (execução local, testes e deploy) está no [final do documento](#informações-técnicas).

Projeto Integrador — Innovation Lab: Advanced No/Low Code — ADS, Faculdade Impacta, 2026.2.

## Sumário

1. [Apresentação](#1-apresentação)
2. [Acesso ao aplicativo](#2-acesso-ao-aplicativo)
3. [Perfis de usuários](#3-perfis-de-usuários)
4. [Funcionalidades](#4-funcionalidades)
5. [Manual de utilização](#5-manual-de-utilização)
6. [Exemplos de utilização](#6-exemplos-de-utilização)
7. [Limitações conhecidas](#7-limitações-conhecidas)
8. [Informações técnicas](#informações-técnicas)

## 1. Apresentação

**O que é.** O StudyMatch é uma aplicação web que conecta alunos com dificuldades acadêmicas em comum para estudarem juntos.

**Problema.** Quem tem dificuldade em uma disciplina muitas vezes estuda sozinho, por não saber quais colegas enfrentam a mesma dificuldade e têm horários compatíveis. Formar grupos de estudo depende de contatos informais.

**Solução.** O aluno informa as disciplinas em que tem dificuldade e os horários livres, e o sistema sugere colegas compatíveis, com um percentual. Quando os dois demonstram interesse, o match é confirmado e eles podem conversar pelo site ou pelo WhatsApp.

**Público-alvo.** Estudantes que procuram companhia para estudar disciplinas do próprio curso.

## 2. Acesso ao aplicativo

**Link:** https://studymatch-y50f.onrender.com/

- Não é preciso instalar nada. Basta um navegador e conexão com a internet.
- Se o site estiver sem uso há algum tempo, o primeiro acesso demora cerca de um minuto.
- Desative a tradução automática do navegador, porque ela pode trocar os nomes das telas e dos botões.
- Para usar, crie uma conta ou entre com o e-mail e a senha do seu cadastro.
- Recarregar a página (F5) encerra a sessão: é preciso entrar de novo.

## 3. Perfis de usuários

| Perfil | Descrição | Responsabilidades | Permissões |
|---|---|---|---|
| **Aluno** | Usuário principal do site | Manter perfil, disciplinas e horários atualizados e responder aos pedidos recebidos | Alterar apenas os próprios dados; ver colegas compatíveis; enviar, cancelar, aceitar e recusar interesses; ver o telefone e conversar depois do match |
| **Administrador** | Responsável pelos dados acadêmicos | Manter o cadastro de cursos e disciplinas | Incluir e editar cursos e disciplinas, somente pelo painel do Xano (não há tela de administração no site) |

O telefone de um aluno só aparece para colegas com match confirmado. O e-mail não aparece para os colegas.

## 4. Funcionalidades

- **Conta:** cadastro em 3 etapas, login e logout.
- **Perfil:** dados pessoais, foto e texto "Sobre mim".
- **Disciplinas:** escolha das disciplinas do próprio curso em que o aluno tem dificuldade.
- **Disponibilidade:** horários livres por dia da semana.
- **Busca de colegas:** lista com percentual de compatibilidade, busca por matéria, filtro por semestre e ordenação.
- **Interesse e match:** enviar, cancelar, aceitar ou recusar.
- **Contato:** conversa por texto no site e botão para o WhatsApp com mensagem pronta.
- **Aparência:** modo claro e modo escuro.

### Como a compatibilidade é calculada

O percentual vai de 0 a 100: **60% pelas disciplinas em comum** e **40% pelos horários em comum**. Só aparecem colegas com pelo menos uma disciplina de dificuldade em comum.

- Disciplinas: quantidade em comum ÷ quantidade de quem tem menos disciplinas.
- Horários: minutos em comum na semana ÷ minutos de quem tem menos tempo disponível.

## 5. Manual de utilização

### Aluno

#### 5.1 Criar conta

1. Na tela de entrada, clique em **Criar conta**.
2. Informe nome e sobrenome e clique em **Avançar**.
3. Crie uma senha com pelo menos 8 caracteres, com letras e números, confirme a senha, informe o e-mail e clique em **Avançar**.
4. Escolha o curso e o semestre, informe o telefone e, se quiser, escreva o "Sobre mim".
5. Clique em **Criar conta**.

**Resultado esperado:** o aluno entra no sistema e vê a página Início.

**Se der erro:** o e-mail e o telefone não podem pertencer a outra conta. A mensagem mostra qual dado corrigir.

#### 5.2 Entrar e sair

1. Informe o e-mail e a senha e clique em **Entrar** (ou pressione Enter).
2. Para encerrar, clique em **Sair** no menu lateral.

**Resultado esperado:** com os dados corretos, a página Início abre. Com dados errados, aparece "E-mail ou senha inválidos.".

#### 5.3 Completar o perfil

Abra **Meu perfil** no menu lateral.

1. **Disciplinas:** escolha as disciplinas em que tem dificuldade e clique em **Salvar disciplinas**.
2. **Disponibilidade:** escolha o dia, o início e o fim e clique em **Adicionar horário**. Repita para cada horário livre. Para excluir um horário, clique em **Remover**.
3. **Dados:** altere o que precisar e clique em **Salvar dados**. O e-mail não pode ser alterado.
4. **Foto (opcional):** na aba Dados, clique em **Adicionar foto**, escolha uma imagem JPG, PNG ou WEBP de até 2 MB e clique em **Salvar foto**.

**Resultado esperado:** cada alteração mostra uma confirmação, como "Disciplinas salvas.", e o painel "Seu perfil" no Início mostra quanto do perfil está completo.

**Atenção:** trocar de curso remove as disciplinas escolhidas. Horários no mesmo dia não podem se sobrepor, e o fim deve ser depois do início.

#### 5.4 Encontrar colegas

1. Abra **Início**. Cada cartão mostra o percentual, as disciplinas e os horários em comum.
2. Se quiser, busque por matéria, filtre por semestre ou mude a ordem da lista.
3. Clique em **Ver perfil** para ver os detalhes do colega.
4. Clique em **Dar match** para demonstrar interesse.

**Resultado esperado:** aparece "Interesse enviado para (nome)." e o cartão passa a mostrar que aguarda resposta. Se o colega já tinha enviado interesse, o botão é **Aceitar interesse** e o match é confirmado na hora.

#### 5.5 Responder e acompanhar pedidos

Abra **Meus matches**. Use **Atualizar** para ver novidades.

| Aba | O que mostra | O que fazer |
|---|---|---|
| **Recebidos** | Colegas que querem estudar com você | **Aceitar** ou **Recusar** |
| **Enviados** | Interesses que você enviou | **Cancelar interesse**, enquanto não houver resposta |
| **Confirmados** | Colegas com match | Ver o telefone, **Conversar** ou **Chamar no WhatsApp** |

**Resultado esperado:** ao aceitar, o colega passa para a aba Confirmados e o telefone dele é liberado. Ao recusar, quem enviou vê "Este colega recusou o seu interesse.".

#### 5.6 Conversar com o colega

1. Em **Meus matches**, abra a aba **Confirmados** e clique em **Conversar**.
2. Escreva uma mensagem de até 500 caracteres e envie.
3. Para voltar, clique em **Voltar para Meus matches**.

**Resultado esperado:** a mensagem enviada aparece na hora, e as do colega chegam em alguns segundos, sem recarregar a página. Só os dois alunos do match podem ler e enviar mensagens na conversa.

Como alternativa, **Chamar no WhatsApp** abre o WhatsApp com uma mensagem pronta que cita as disciplinas em comum.

#### 5.7 Mudar a aparência

Use o botão de modo claro ou escuro, na tela de entrada ou no menu lateral.

**Resultado esperado:** as cores do site mudam imediatamente.

### Administrador

#### 5.8 Manter cursos e disciplinas

1. Entre no painel do Xano com uma conta autorizada no projeto.
2. Abra a tabela `curso` ou `disciplina`.
3. Inclua ou edite o registro. Cada disciplina deve estar ligada a um curso.

**Resultado esperado:** os cursos ficam disponíveis no cadastro e no perfil, e as disciplinas na aba Disciplinas dos alunos daquele curso. A mudança pode levar até 10 minutos para aparecer no site.

## 6. Exemplos de utilização

Os nomes abaixo são fictícios. Os dois alunos são de Análise e Desenvolvimento de Sistemas.

| Aluno | Disciplinas de dificuldade | Horário livre |
|---|---|---|
| Ana | Fundamentos de SQL e Engenharia de Software | Segunda, 19:00 às 21:00 |
| Bruno | Fundamentos de SQL | Segunda, 20:00 às 22:00 |

### Cenário 1: do cadastro à conversa

1. Ana e Bruno criam as contas e cadastram as disciplinas e os horários da tabela.
2. No Início, Ana vê Bruno com **80%**: 60 pontos, porque a única disciplina de Bruno também é de Ana, e 20 pontos, porque metade do horário coincide.
3. Ana clica em **Dar match**.
4. Bruno abre **Meus matches**, aba **Recebidos**, e clica em **Aceitar**.
5. Os dois veem o telefone um do outro em **Confirmados** e clicam em **Conversar** para combinar o estudo.

### Cenário 2: disciplina em comum sem horário em comum

Se Bruno só estivesse livre na terça, ele continuaria na lista de Ana, com **60%**.

### Cenário 3: nenhuma disciplina em comum

Se a única dificuldade de Bruno fosse Programação e Algoritmos, ele não apareceria na lista de Ana, mesmo com os mesmos horários.

### Cenário 4: pedido recusado

Bruno clica em **Recusar**. Em **Enviados**, Ana vê "Este colega recusou o seu interesse.". Nenhum telefone é liberado e não há conversa.

### Cenário 5: horário inválido

Ana tenta adicionar segunda das 20:00 às 22:00. Como já tem segunda das 19:00 às 21:00, aparece "Este horário se sobrepõe a outra disponibilidade sua." e nada é gravado.

## 7. Limitações conhecidas

**Não implementado**
- Recuperação de senha e alteração de e-mail ou senha.
- Exclusão da conta pela tela (existe apenas na API).
- Notificações por e-mail ou push.
- Grupos com mais de duas pessoas.
- Tela de administração: cursos e disciplinas são mantidos pelo painel do Xano.
- Na conversa: anexos, edição, exclusão de mensagens, bloqueio e denúncia.

**Restrições de acesso**
- Só é possível escolher disciplinas do próprio curso.
- O telefone e a conversa exigem match confirmado.

**Limitações da versão atual**
- A conversa não é em tempo real: a tela busca mensagens novas a cada 8 segundos e, ao abrir, mostra as últimas 50.
- As listas de colegas e de matches não se atualizam sozinhas: use os botões de atualizar.
- O plano gratuito do Xano aceita 10 requisições a cada 20 segundos, e cada conversa aberta gasta de 2 a 3. Com vários acessos ao mesmo tempo, o site pode demorar a responder.
- O plano gratuito do Render desliga o site depois de um tempo sem acesso, e o próximo acesso demora cerca de um minuto.
- Recarregar a página encerra a sessão.

## Informações técnicas

- **Backend:** [Xano](https://www.xano.com/) (banco, API REST e autenticação). O código XanoScript fica em [`xano/`](xano/).
- **Frontend:** [Streamlit](https://streamlit.io/), que só consome a API do Xano.
- **Especificação:** [OpenSpec](openspec/). As specs consolidadas ficam em `openspec/specs/` e o histórico de changes em `openspec/changes/archive/`.
- **Contexto do projeto:** [`docs/project-overview.md`](docs/project-overview.md), [`docs/domain-model.md`](docs/domain-model.md) e [`AGENTS.md`](AGENTS.md).

### Estrutura

```text
app.py                 ponto de entrada (navegação conforme o login)
paginas/               telas: entrar, cadastro (3 etapas), início (busca de colegas), matches, conversa, perfil, sair
studymatch/            cliente da API (api.py), sessão (sessao.py), rótulos (dominio.py) e visual (visual.py)
assets/                CSS e logos do tema (referência: protótipo no Figma)
tests/api/             testes de API contra o Xano
tests/frontend/        testes do cliente (offline) e das telas (AppTest)
xano/                  workspace do Xano em XanoScript (sincronizado com o Xano CLI)
render.yaml            Blueprint de deploy no Render
```

### Rodar localmente

Pré-requisito: Python 3.14 (a mesma versão de `.python-version`).

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    |    Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

Configure a URL da API do Xano: copie `.streamlit/secrets.toml.example` para `.streamlit/secrets.toml` e preencha `XANO_API_URL`. Ela é a URL base do grupo de API **Authentication**, no formato `https://<instancia>.xano.io/api:<canonical>`. O `secrets.toml` é ignorado pelo Git. Em vez dele, também dá para usar a variável de ambiente `XANO_API_URL`, que tem prioridade.

```bash
streamlit run app.py
```

O app abre em http://localhost:8501.

### Testes

Os testes de API e de tela rodam contra o Xano de verdade: criam alunos de teste (`teste.*@studymatch.test`) e apagam todos no final. O plano free do Xano aceita 10 requisições a cada 20 s, por isso os testes esperam entre as chamadas e levam alguns minutos.

```bash
python tests/frontend/teste_api_cliente.py   # cliente da API, offline e rápido
python tests/api/teste_seguranca.py          # autenticação e controle de acesso
python tests/api/teste_perfil.py             # perfil, disciplinas e disponibilidade
python tests/api/teste_busca.py              # compatibilidade e interesse
python tests/api/teste_matches.py            # meus matches e telefone após o match
python tests/api/teste_chat.py               # conversa do match (envio, leitura, acesso, exclusão)
python tests/api/teste_foto.py               # foto de perfil (envio, troca, remoção)
python tests/frontend/teste_telas_base.py    # login, cadastro e logout
python tests/frontend/teste_telas_perfil.py
python tests/frontend/teste_telas_busca.py
python tests/frontend/teste_telas_matches.py
python tests/frontend/teste_telas_chat.py
python tests/frontend/teste_telas_tema.py     # modo claro/escuro
```

Por padrão, os testes usam a API do projeto. Para apontar para outra, defina `XANO_API_URL`.

### Backend (Xano)

As alterações no backend são feitas nos arquivos `.xs` em `xano/` e publicadas com o [Xano CLI](https://docs.xano.com/):

```bash
cd xano
xano workspace push --dry-run   # revise a prévia
xano workspace push             # publica só os arquivos alterados
```

Depois do push, rode `xano workspace pull` em uma pasta temporária e copie o resultado para `xano/`. Assim o formato local fica idêntico ao do servidor.

### Deploy no Render

O repositório já tem o Blueprint [`render.yaml`](render.yaml): um web service Python no plano free, que instala `requirements.txt`, sobe o Streamlit em `0.0.0.0:$PORT` e usa `/_stcore/health` como health check. A versão do Python vem de `.python-version`.

1. Entre no [Render](https://dashboard.render.com/) e conecte a sua conta do GitHub.
2. Clique em **New → Blueprint** e escolha o repositório `studymatch` (branch `main`).
3. O Render lê o `render.yaml` e pede o valor de **`XANO_API_URL`**. Informe a URL base da API (a mesma do `secrets.toml`).
4. Clique em **Apply**. O primeiro build leva alguns minutos. Quando terminar, o app fica em https://studymatch-y50f.onrender.com/.
5. A cada commit na `main`, o Render faz um novo deploy automaticamente (`autoDeployTrigger: commit`).

Observações:
- No plano free, o serviço "dorme" depois de um tempo sem acesso. O primeiro acesso seguinte demora cerca de um minuto.
- Para trocar a URL da API depois, vá em **Environment** no painel do serviço e altere `XANO_API_URL`.
- Sem o Blueprint, dá para criar um **Web Service** manualmente com os mesmos comandos: build `pip install -r requirements.txt` e start `streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`.
