# Mini – PromptOS com FastAPI

Projeto backend com estrutura modular, agentes integrados e deploy automatizado no Railway.

---

## Rodando localmente (Docker)

1. Clone o repositório:

```bash
git clone https://github.com/voulezvous-ai/mini.git
cd mini
```

2. Copie as variáveis de ambiente:

```bash
cp .env.example .env
```

3. Inicie os serviços:

```bash
docker-compose up --build
```

---

## Deploy no Railway

- Certifique-se de ter o `Dockerfile` na raiz
- Variável `PORT=8000` configurada nas settings do Railway
- Backend em `/backend/main.py` com Uvicorn apontando para `main:app`

---

## Estrutura

- `backend/` — aplicação principal FastAPI
- `modules/` — funcionalidades por agente
- `frontend/` — React (opcional)

---

## Variáveis de ambiente importantes

- `MONGODB_URI` — string de conexão com banco
- `SECRET_KEY` — usada para autenticação e segurança