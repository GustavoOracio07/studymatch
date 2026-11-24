# Design

## Context

Motivação em `proposal.md`. O frontend é só Streamlit e fala com o Xano por REST. O plano free aceita 10 requisições a cada 20 s. `XanoAPI._req` espera 2, 4 e 8 s após um 429, o que congelaria a tela se usado na busca automática.

## Goals / Non-Goals

**Goals:**
- Conversa entre duas contas fluida o bastante para gravar o vídeo.
- Regras de acesso inteiramente no Xano.

**Non-Goals:**
- Suportar muitas conversas simultâneas no plano free.

## Decisions

- **`mensagem` guarda `match_interesse_id`, `remetente_id` e `destinatario_id`.** O backend deduz os dois alunos do match. O destinatário permite apagar por aluno com um único `db.bulk.delete`, dentro da transação de `excluir_usuario`. Alternativa: percorrer os matches do aluno, com mais consultas.
- **Busca incremental por id (`depois_de`).** Evita baixar a conversa inteira. Índice em `match_interesse_id` + `id`. Alternativa: filtrar por data, sujeita a empates.
- **`st.fragment(run_every=8)`.** Atualiza só a lista de mensagens. Cada tela gasta 2,5 requisições a cada 20 s; duas gastam 5. Alternativas: 2 s (uma tela já atinge o limite) e 5 s (testado com duas contas: o limite estourou em uma conversa normal). Um componente WebSocket exigiria outro serviço.
- **Mensagem enviada entra na tela pela resposta do `POST`.** Dispensa a busca logo após o envio, exceto se a última já passou do intervalo. O cursor da busca só avança com o que vem do `GET`, para não pular mensagens do colega.
- **Sem novas tentativas na busca automática.** `_req` ganha um parâmetro para desligar as esperas; a próxima busca já é a nova tentativa. Envios mantêm as esperas.
- **Mensagens na sessão, por match.** Guardadas sem repetir ids e descartadas no logout.
- **`st.text` dentro de `st.chat_message`.** Mostra o conteúdo literal, sem HTML ou Markdown.
- **Página fora do menu.** A conversa depende de um match escolhido, guardado na sessão.

## Risks / Trade-offs

- [O limite do Xano pode ser compartilhado por todo o site; 5 telas de conversa abertas já pedem 12,5 requisições a cada 20 s] → aviso na tela, sem travar; limitação registrada no README. No vídeo, usar só duas contas e poucas mensagens.
- [Um envio pode falhar depois de 14 s de espera] → a tela mostra o erro e o texto precisa ser reenviado.
- [Conversa sem bloqueio nem denúncia] → só alunos que confirmaram o match conversam; fica para evolução futura.

## Migration Plan

1. Publicar primeiro o Xano (mudança só de adição, compatível com o site atual) e testar a API.
2. Publicar o frontend.
3. Para voltar atrás, reverter o frontend. A tabela pode ficar sem uso.
