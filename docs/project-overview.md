# Project Overview — StudyMatch

## 1. Visão geral
StudyMatch é uma aplicação web que conecta estudantes com dificuldades acadêmicas em comum para que estudem juntos. O sistema cruza as disciplinas em que cada aluno tem dificuldade e os horários disponíveis, e sugere colegas compatíveis.

Projeto Integrador da disciplina Innovation Lab: Advanced No/Low Code — ADS, Faculdade Impacta, 2026.2.

## 2. Problema
Alunos com dificuldade em uma disciplina muitas vezes estudam sozinhos por não saberem quais colegas enfrentam a mesma dificuldade e têm horários compatíveis. Formar grupos de estudo depende de contatos informais.

## 3. Objetivos
- Permitir que o aluno registre as disciplinas em que tem dificuldade e seus horários livres.
- Sugerir colegas compatíveis, com um percentual de compatibilidade.
- Permitir que os alunos demonstrem interesse uns nos outros e confirmem o match.
- Após o match, permitir que os alunos entrem em contato para estudar juntos.

## 4. Público-alvo / usuários
- **Aluno:** usuário principal. Cadastra-se, informa curso, semestre, disciplinas de dificuldade e disponibilidade, e interage com sugestões de match.
- **Administrador:** mantém o cadastro de cursos e disciplinas apenas pelo painel do Xano. Qualquer pessoa pode ler cursos e disciplinas; ninguém os edita pelo app.

## 5. Escopo
**Dentro do escopo inicial:**
- Cadastro e login de alunos.
- Perfil do aluno (curso, semestre, contato, sobre mim).
- Seleção das disciplinas de dificuldade.
- Cadastro de disponibilidade (dia da semana e faixa de horário).
- Sugestão de colegas compatíveis com percentual.
- Interesse em um colega e resposta (aceitar/recusar), gerando match.

**Fora do escopo inicial:**
- Chat dentro do sistema.
- Grupos com mais de duas pessoas.
- Notificações por e-mail/push.
- Cadastro de cursos e disciplinas pela interface.
- Recuperação de senha por e-mail.

## 6. Principais funcionalidades
- Autenticação (cadastro, login, logout).
- Gestão do perfil do aluno.
- Gestão de disciplinas de dificuldade do aluno.
- Gestão de disponibilidade do aluno.
- Sugestão de matches compatíveis.
- Interesse, aceite e recusa de match.
- Listagem dos matches confirmados com contato.

## 7. Requisitos e restrições importantes
- Um aluno não pode demonstrar interesse em si mesmo.
- Um aluno não pode demonstrar interesse duas vezes no mesmo colega.
- O percentual de compatibilidade fica entre 0 e 100.
- Na disponibilidade, a hora de fim deve ser maior que a hora de início.
- E-mail e telefone são únicos por usuário.
- Semestre entre 1 e 12.
- Interface e dados em português brasileiro.

## 8. Arquitetura tecnológica
- **Backend:** Xano (banco de dados, API REST e autenticação).
- **Frontend:** Streamlit, como tecnologia exclusiva do frontend.
- **Especificação:** OpenSpec (schema spec-driven).
- **Versionamento:** Git + GitHub.
- **Deploy:** Render.
- **Agente de IA:** GitHub Copilot (modo Agent) com Xano Developer MCP.

O banco já está estruturado no Xano com 6 tabelas: curso, disciplina, user, usuario_disciplina, disponibilidade e match_interesse. Algumas validações já existem nos endpoints.

## 9. Princípios de desenvolvimento
- Especificar antes de implementar.
- Entregas incrementais e verticais (backend + tela juntos).
- O banco evolui junto com as funcionalidades.

## 10. Segurança e integridade
- Regras de negócio e autorização ficam no Xano.
- Cada aluno só altera os próprios dados.
- O telefone só é exibido após match confirmado.

## 11. Estratégia de desenvolvimento
Desenvolvimento por changes do OpenSpec, com revisão do grupo antes de cada implementação. Apresentação final em 27/11/2026.

## 12. Fonte de verdade e documentação
- Visão do projeto: este documento.
- Conceitos do domínio: `docs/domain-model.md`.
- Comportamento consolidado: `openspec/specs/`.
- Mudanças em andamento: `openspec/changes/`.
