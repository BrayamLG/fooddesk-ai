# Publicação segura no GitHub

Este roteiro assume que o repositório ainda não foi publicado. Se você já fez commit da chave que estava no arquivo `secrets.toml`, siga também a seção **Se a chave já foi publicada**.

## 1. Revogue a chave que foi compartilhada

1. Abra o Google AI Studio e localize a chave usada pelo projeto.
2. Revogue/exclua a chave antiga.
3. Gere uma chave nova.
4. Não cole a chave em issues, README, capturas de tela ou mensagens.
5. Guarde a chave nova somente no arquivo local `.streamlit/secrets.toml` ou no gerenciador de segredos do ambiente de deploy.

Apagar o arquivo do projeto não invalida uma chave que já foi exposta.

## 2. Prepare a pasta local

1. Baixe e extraia o ZIP revisado.
2. Abra a pasta `fooddesk-ai` no VS Code.
3. Confirme que `.streamlit/secrets.toml` **não existe**. O arquivo `secrets.toml.example` é apenas um modelo sem segredo.
4. Se quiser executar localmente, copie `.streamlit/secrets.toml.example` para `.streamlit/secrets.toml` e adicione a chave nova. Esse arquivo é ignorado pelo Git.
5. Crie um ambiente virtual e instale as dependências, conforme o README.
6. Execute os testes:

   ```bash
   pip install -r requirements-dev.txt
   pytest -q
   ```

7. Rode a aplicação localmente:

   ```bash
   streamlit run app.py
   ```

8. Teste os três cenários de avaliação, o dashboard, o simulador e a página de sanitização. Teste o webhook apenas com um endpoint de demonstração que você controla.

## 3. Faça uma última checagem antes do Git

No terminal do VS Code, a partir da pasta do projeto:

```bash
git status --short
git check-ignore -v .streamlit/secrets.toml
```

O segundo comando deve mostrar uma regra do `.gitignore` para o arquivo local de segredos, caso esse arquivo exista.

Se o Git ainda não foi inicializado, `git status` mostrará que não é um repositório; isso é esperado nesta etapa. Antes de criar o commit, confira visualmente a lista de arquivos. Não adicione `.streamlit/secrets.toml`, `.env`, tokens, chaves ou arquivos de conta de serviço.

## 4. Crie o repositório no GitHub

1. No GitHub, crie um repositório chamado `fooddesk-ai`.
2. Para facilitar o primeiro push, crie-o vazio: não marque as opções de criar README, `.gitignore` ou licença, pois esses arquivos já estão no projeto.
3. Não adicione credenciais como secrets do repositório para apenas publicar o código.
4. Copie a URL HTTPS do novo repositório.

## 5. Inicialize e publique

Execute os comandos a seguir na pasta raiz do projeto. Substitua a URL pela URL real do seu repositório:

```bash
git init
git add .
git status --short
git diff --cached --name-only
```

**Pare e revise a lista antes de continuar.** Se aparecer `secrets.toml`, `.env` ou qualquer arquivo com credenciais, não faça commit. Corrija o `.gitignore`, retire o arquivo do stage e confira novamente.

Se a lista estiver limpa:

```bash
git commit -m "Prepare FoodDesk AI portfolio project"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/fooddesk-ai.git
git push -u origin main
```

Se o Git solicitar autenticação, use o fluxo de autenticação do GitHub; não coloque tokens no comando nem no código.

## 6. Depois da publicação

- Abra o repositório em uma janela anônima para conferir como recrutadores o verão.
- Revise o README no próprio GitHub, inclusive os comandos de instalação.
- Confira se o workflow de testes executou na aba **Actions**.
- Ative os recursos de segurança disponíveis nas configurações do repositório, incluindo alertas de segredos e dependências quando disponíveis.
- Adicione capturas de tela da aplicação com dados fictícios, sem chaves ou URLs privadas.
- Não publique uma instância pública com sua própria chave de API sem limites de uso, controle de custos e proteção contra abuso. O código atual é um protótipo e não inclui rate limiting de produção.
- Se publicar uma demo, configure segredos na plataforma de deploy, nunca no código. Lembre que usuários públicos podem consumir sua quota de API.

## Se a chave já foi publicada em um commit

1. Revogue a chave imediatamente; considere-a comprometida.
2. Remova o arquivo do código atual e adicione-o ao `.gitignore`.
3. Se necessário, reescreva o histórico com uma ferramenta apropriada como `git filter-repo` e force-push seguindo o procedimento oficial do GitHub.
4. Avise colaboradores para sincronizarem o histórico reescrito.
5. Verifique logs, forks e caches conforme as opções do provedor. A reescrita do histórico não substitui a revogação da chave.

## Limite desta revisão

A revisão inclui análise estática, compilação dos arquivos Python e testes unitários das funções de segurança. Não equivale a um pentest, não garante segurança absoluta e não substitui uma revisão independente antes de usar dados reais.
