# FoodDesk AI

**Inteligência aplicada a operações e experiência do cliente.**

## 🚀 Demonstração online

**[Acesse o FoodDesk AI](https://fooddesk-ai.streamlit.app/)**

Experimente a plataforma demonstrativa diretamente pelo navegador.

[Ver código-fonte no GitHub](https://github.com/BrayamLG/fooddesk-ai)

O FoodDesk AI é um projeto experimental de portfólio que demonstra como conceitos de inteligência artificial, automação e análise de dados podem ser aplicados a uma operação de atendimento e experiência do cliente.

Desenvolvido em Python com Streamlit, o projeto utiliza um fluxo demonstrativo executado localmente, sem chamadas a modelos de IA, APIs externas ou webhooks.

> **Importante:** projeto independente, sem vínculo oficial com o iFood ou qualquer outra empresa.

## Problema

Operações de atendimento recebem avaliações e comentários que podem revelar problemas recorrentes, como atrasos, itens faltantes, qualidade dos produtos e falhas de embalagem.

O FoodDesk AI simula o processo de transformar esses registros em informações organizadas e recomendações que apoiem a tomada de decisão.

## Funcionalidades

- Análise demonstrativa de avaliações por regras locais.
- Fluxo de processamento com recebimento, sanitização, análise simulada, validação e recomendação.
- Dashboard executivo com indicadores e visualizações.
- Histórico de avaliações processadas durante a sessão.
- Simulador ilustrativo de impacto operacional.
- Demonstração de sanitização e mascaramento de informações.

## Como funciona

1. **Recebimento:** a aplicação recebe a nota e o comentário.
2. **Proteção:** o texto passa por regras locais de sanitização.
3. **Análise simulada:** regras determinísticas classificam a avaliação. Nenhum modelo de IA é chamado nesta versão.
4. **Validação:** a estrutura e os campos do resultado são verificados.
5. **Recomendação:** a aplicação apresenta uma sugestão de ação.

### Arquitetura simplificada

```text
Avaliação do cliente
        |
        v
Recebimento dos dados
        |
        v
Sanitização local
        |
        v
Classificação demonstrativa
        |
        v
Validação da resposta
        |
        v
Diagnóstico e recomendação
        |
        v
Dashboard e histórico
```

## Tecnologias

- Python
- Streamlit
- Pandas
- Altair
- Expressões regulares (Regex)
- JSON
- Unittest

## Estrutura do projeto

```text
fooddesk-ai/
├── .github/
│   └── workflows/
│       └── tests.yml
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml.example
├── tests/
│   ├── test_security_utils.py
│   └── test_workflow_engine.py
├── app.py
├── demo_engine.py
├── workflow_engine.py
├── security_utils.py
├── requirements.txt
├── requirements-dev.txt
├── runtime.txt
├── .gitignore
├── README.md
├── SECURITY.md
└── PUBLISHING.md
```

## Executar localmente

### 1. Clone o repositório

```bash
git clone https://github.com/BrayamLG/fooddesk-ai.git
cd fooddesk-ai
```

### 2. Crie e ative um ambiente virtual

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute a aplicação

```bash
streamlit run app.py
```

A versão demonstrativa não exige chave de API.

## Testes

Execute:

```bash
python -m pytest -v
```

## Privacidade e segurança

A aplicação demonstra:

- Sanitização local de comentários.
- Mascaramento de padrões comuns, como CPF, e-mail e telefone.
- Escape de conteúdo HTML.
- Validação da estrutura dos resultados processados.

**Limitações:** a sanitização por padrões não garante anonimização completa. A classificação utiliza regras e palavras-chave, não compreensão semântica de um modelo de linguagem. A aplicação não implementa autenticação, banco de dados ou monitoramento de produção. Utilize apenas dados fictícios na demonstração.

## Decisões da versão demonstrativa

- Não realiza chamadas a serviços externos.
- Não envia comentários para modelos de IA.
- Não executa webhooks.
- Não exige chave de API.
- Utiliza regras locais para demonstrar o fluxo completo.

O prompt de referência exibido pela aplicação tem finalidade didática: ilustra como uma instrução para um modelo poderia ser estruturada, mas não é enviado a um serviço externo.

## Próximos passos

- Integração opcional com Gemini usando chave configurada localmente.
- Persistência dos registros em banco de dados.
- Ampliação da cobertura de testes.
- Observabilidade e registro de eventos.
- Avaliação adicional de segurança antes de qualquer uso em produção.

---

## Autor

Projeto desenvolvido por **Brayam Gonçalves** como parte de seu aprendizado e construção de portfólio em tecnologia, dados e inteligência artificial.

**FoodDesk AI — Inteligência aplicada a operações e experiência do cliente.**
