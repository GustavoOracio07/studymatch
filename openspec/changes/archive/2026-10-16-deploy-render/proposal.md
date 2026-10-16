# Proposal

## Why

O app precisa estar acessível na web para a apresentação (27/11/2026), e a decisão de deploy é o Render. Hoje o `requirements.txt` está em UTF-16, que o `pip` do Render não lê, e não há configuração de deploy nem instruções no README.

## What Changes

- Converter o `requirements.txt` para UTF-8, mantendo as mesmas versões fixadas.
- Adicionar `.python-version` (3.14), igual ao ambiente local.
- Adicionar `render.yaml` (Blueprint): web service Python no plano free, com `pip install -r requirements.txt`, o Streamlit escutando em `0.0.0.0:$PORT`, health check em `/_stcore/health` e a variável `XANO_API_URL` pedida na criação (sem valor versionado).
- Reescrever o `README.md`: o que é o projeto, como rodar localmente, como rodar os testes e como subir no Render.

**Fora do escopo:**
- Domínio próprio, CI/CD e outro provedor de hospedagem.
- Mudanças de comportamento no app ou no Xano (por isso a change não tem specs: `skip_specs: true`).

## Capabilities

### New Capabilities
<!-- Nenhuma: é configuração de infraestrutura e documentação. -->

### Modified Capabilities
<!-- Nenhuma. -->

## Impact

- Novos arquivos: `render.yaml`, `.python-version`.
- Alterados: `requirements.txt` (só a codificação), `README.md`.
