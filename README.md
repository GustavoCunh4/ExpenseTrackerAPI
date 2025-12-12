## Expense Tracker API

API de rastreamento de despesas pessoais construída com FastAPI, SQLModel e PostgreSQL (compatível com SQLite para desenvolvimento local). Inclui autenticação JWT, separação em camadas (routers → services → repositories), testes com Pytest/HTTPX e configuração pronta para Supabase e deploy na Vercel.

### Requisitos
- Python 3.10+
- Banco PostgreSQL (ex.: Supabase) ou SQLite local
- Pip/venv para dependências

### Configuração rápida
```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows
pip install -r requirements.txt
```

Crie um arquivo `.env` na raiz:
```bash
DATABASE_URL=sqlite+aiosqlite:///./expense.db  # troque pela URL do Supabase em prod
JWT_SECRET=alterar_para_um_segredo_forte
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### Executar localmente
```bash
uvicorn app.main:app --reload
```
Documentação interativa em `http://localhost:8000/docs`.

### Estrutura principal
```
app/
├── api/v1/{auth,categories,expenses}
├── core/{config,db,security}
├── models/{user_model,expense_model,schemas}
├── repositories/{base_repository,user_repository,category_repository,expense_repository}
└── services/{auth_service,category_service,expense_service}
```

### Testes
```bash
pytest
```

### Deploy na Vercel
- Ponto de entrada: `api/index.py`
- Configuração: `vercel.json`
- Defina variáveis de ambiente no painel da Vercel (`DATABASE_URL`, `JWT_SECRET`, `ACCESS_TOKEN_EXPIRE_MINUTES`).

### Fluxo de versionamento sugerido
- Branches: `main` (estável), `develop` (integração), `feature/*`, `fix/*`, `chore/*`.
- Commits no padrão Conventional Commits, ex.: `feat: adiciona resumo mensal de despesas`.

### Integração com PostgreSQL/Supabase
- Use a URL de conexão do Supabase em `DATABASE_URL`.
- Rode as migrations automáticas ao subir a aplicação (tabelas criadas em `startup`).
- Mantenha `.env` fora do versionamento (`.gitignore` já cobre).
