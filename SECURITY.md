# Política de segurança

## Escopo

FoodDesk AI é um protótipo de portfólio. Não deve receber dados pessoais reais nem ser conectado a sistemas de produção.

## Reportar vulnerabilidades

Não publique chaves, tokens, URLs privadas de webhook ou dados pessoais em issues públicas. Para uma cópia pessoal do projeto, corrija imediatamente qualquer credencial exposta e revogue-a no provedor correspondente.

## Controles e limitações conhecidos

- A sanitização usa padrões regex e não garante anonimização completa.
- A saída do modelo é não confiável e precisa ser validada.
- O webhook é restrito a domínios de provedores permitidos e não segue redirecionamentos.
- O projeto não implementa autenticação, rate limiting de produção, auditoria de segurança independente ou monitoramento.
- Não existe garantia de conformidade integral com a LGPD.

## Antes de um deploy público

1. Revogue qualquer chave que já tenha sido compartilhada ou commitada.
2. Configure novos segredos no gerenciador de segredos do ambiente de deploy.
3. Confirme que o segredo não aparece no histórico do Git.
4. Execute os testes e revise as dependências.
5. Use dados sintéticos e faça uma revisão independente.
