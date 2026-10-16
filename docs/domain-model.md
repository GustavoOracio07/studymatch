# Domain Model — StudyMatch

Modelo conceitual. Os nomes entre parênteses são as tabelas atuais no Xano.

```text
Curso
  ├── Disciplina
  └── Aluno (user)
        ├── Dificuldade em Disciplina (usuario_disciplina) ──► Disciplina
        ├── Disponibilidade (disponibilidade)
        └── Interesse de Match (match_interesse) ──► outro Aluno
```

## Curso (`curso`)
Curso de graduação oferecido pela faculdade (ex.: ADS).
- **Informações:** nome.
- **Relacionamentos:** um curso possui várias disciplinas e vários alunos.

## Disciplina (`disciplina`)
Matéria que pertence a um curso.
- **Informações:** nome, curso.
- **Relacionamentos:** pertence a um único curso. Pode ser marcada como dificuldade por vários alunos.

## Aluno (`user`)
Estudante que usa o sistema. Usa a tabela de autenticação do Xano.
- **Informações:** nome, sobrenome, e-mail, senha, telefone/contato, curso, semestre, sobre mim.
- **Regras:** e-mail único; telefone único; semestre de 1 a 12.
- **Relacionamentos:** pertence a um curso; tem várias dificuldades, várias disponibilidades e vários interesses de match.

## Dificuldade em Disciplina (`usuario_disciplina`)
Associação N:N que indica que um aluno tem dificuldade em uma disciplina.
- **Informações:** aluno, disciplina.
- **Regras:** o mesmo aluno não repete a mesma disciplina; o aluno só pode escolher disciplinas do próprio curso.

## Disponibilidade (`disponibilidade`)
Faixa de horário em que o aluno pode estudar.
- **Informações:** aluno, dia da semana (segunda a domingo), hora de início, hora de fim.
- **Regras:** horas no formato HH:MM; hora de fim maior que hora de início (a faixa não atravessa a meia-noite); faixas sobrepostas do mesmo aluno não são permitidas.

## Interesse de Match (`match_interesse`)
Registro de que um aluno demonstrou interesse em estudar com outro.
- **Informações:** aluno de origem, aluno alvo, percentual de compatibilidade (0 a 100), status.
- **Status:** `pendente` (interesse enviado) → `match` (alvo aceitou) ou `recusado` (alvo recusou).
- **Regras:** não pode ter o mesmo aluno como origem e alvo; não pode repetir o par origem/alvo.
- **Relacionamentos:** referencia dois alunos.

## Decisões do domínio
- **Cálculo da compatibilidade:** 60% pelas disciplinas de dificuldade em comum e 40% pelos horários de disponibilidade em comum. Curso não entra no cálculo (a regra de disciplina já garante o mesmo curso); semestre fica fora do MVP.
- **Par ou grupo:** o MVP suporta apenas pares. Grupos ficam para uma versão futura.
- **Interesse cruzado:** se A já enviou interesse para B, B não cria um novo registro; B apenas aceita o interesse existente, que passa para `match`.
