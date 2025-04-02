# PromptOS

PromptOS é um microsserviço autossustentável e production-ready para prototipagem de ideias – "o que você quiser em 5 minutos". O sistema foi desenvolvido com uma estrutura modular robusta, integração com CI/CD, containerização e monitoramento avançado.

---

## Arquitetura do Projeto

```
.
├── .env.example                      # Exemplo de variáveis de ambiente
├── .github
│   └── workflows
│       └── ci-cd.yml                # Pipeline CI/CD com GitHub Actions (pytest, flake8)
├── Dockerfile                        # Configuração do container
├── docker-compose.yml                # Orquestração com MongoDB, Redis, etc.
├── agent                             # Lógica central dos agentes
│   ├── engine.py                    # Interpreta prompts e dispara ações
│   ├── feedback.py                  # Estiliza a resposta para o usuário
│   └── main.py                      # API FastAPI (inclui endpoints protegidos)
├── config
│   ├── railway.json                 # Configuração para Railway
│   └── requirements.txt             # Dependências Python
├── docs                              # Documentação gerada com Sphinx
│   ├── README.md
│   └── conf.py
├── frontend                          # Painel frontend em React
│   ├── package.json
│   ├── public
│   │   └── index.html
│   └── src
│       ├── App.js
│       └── index.js
├── interface
│   ├── cli.py                       # Interface interativa via CLI
│   └── voice.py                     # Integração real de TTS (usando gTTS)
├── memory                            # Logging e persistência
│   ├── agentos.log                  # Log gerado automaticamente
│   ├── logger.py                    # Configuração do Loguru
│   └── mongo.py                     # Conexão com MongoDB
├── reasoning                        # Tratamento global de exceções
│   └── error_handler.py
├── scheduler                        # Agendamento de tarefas com Celery Beat
│   ├── celery_app.py
│   └── tasks.py
├── tests                            # Testes automatizados com pytest
│   ├── tests
│   │   └── test_status.py
│   ├── main.py
│   ├── stt_tts.py
│   └── test_voice.py
└── tools                            # Ações e integração com LLM
    ├── actions
    │   ├── generate_architecture.py
    │   ├── push_zip.py
    │   └── sync_env.py
    └── llm.py
```

---

## Funcionalidades Principais

- **Estrutura Modular:** Separação clara entre agentes, interfaces, ferramentas, memória e scheduler.
- **Deploy Automatizado:** Pipeline CI/CD via GitHub Actions e deploy com Docker/Docker Compose.
- **Monitoramento e Logging:** Loguru com rotação automática e integração com Sentry para captura de erros.
- **Agendamento de Tarefas:** Health check e limpeza de logs executados periodicamente via Celery Beat.
- **Interface de Prompt:** Endpoint `/prompt` para envio de comandos via API, protegido por API key.
- **Painel Frontend:** Interface em React para envio de prompts e visualização de respostas.
- **Integração TTS Real:** O módulo de voz utiliza o gTTS para converter texto em fala real.

---

## Como Iniciar

1. **Configurar Variáveis de Ambiente:**  
   Copie o arquivo `.env.example` para `.env` e defina as chaves:
   - `OPENAI_API_KEY`
   - `MONGODB_URI`
   - `CELERY_BROKER_URL`
   - `CELERY_RESULT_BACKEND`
   - `SENTRY_DSN`
   - `API_KEY` (para proteger os endpoints)

2. **Instalar Dependências e Iniciar o Container:**
   ```bash
   docker-compose up --build
   ```

   A aplicação ficará disponível em http://localhost:8000.

3. **Frontend:**
   Navegue até o diretório frontend, instale as dependências e inicie:
   ```bash
   cd frontend
   npm install
   npm start
   ```
   O painel React estará disponível (por padrão em http://localhost:3000).

4. **Documentação:**
   Em docs/, execute:
   ```bash
   make html
   ```
   A documentação gerada ficará em docs/_build/html/index.html.

5. **Testes Automatizados:** Execute os testes com:
   ```bash
   pytest
   ```

## CI/CD e Deploy

- **GitHub Actions:** Verifica código com pytest e flake8 a cada push.
- **Deploy:** A integração com Railway pode ser configurada para deploy automático usando o arquivo config/railway.json.

## Contribuição

Sinta-se à vontade para expandir os módulos, adicionar novos agentes ou integrar outras soluções de TTS e LLM. Todas as sugestões são bem-vindas!

## Contato

Em caso de dúvidas ou sugestões, abra uma issue ou entre em contato.

Este README oficial foi gerado para refletir a versão production-ready do PromptOS, consolidando todas as melhorias e integrações propostas.