# Arquitetura do Evolua

## Visão Geral

O Evolua é uma aplicação web de fitness com arquitetura cliente-servidor, separando completamente a camada de apresentação (frontend) da lógica de negócio (backend).

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  Cliente (Navegador)                                       │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  Frontend (HTML/CSS/JavaScript)                     │  │
│  │  - index.html (UI)                                  │  │
│  │  - styles.css (Styling)                             │  │
│  │  - app.js (Lógica da aplicação)                     │  │
│  │  - api.js (Cliente HTTP)                            │  │
│  └─────────────────────────────────────────────────────┘  │
│                          ↕ HTTP/JSON                       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  Servidor (Backend - Python Flask)                         │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  app.py (Rotas e Endpoints da API)                 │  │
│  │  - Users                                            │  │
│  │  - Exercises                                        │  │
│  │  - Plans                                            │  │
│  │  - Workouts                                         │  │
│  │  - Progress                                         │  │
│  │  - Medals                                           │  │
│  └─────────────────────────────────────────────────────┘  │
│                          ↕                                 │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  models.py (Modelos SQLAlchemy)                    │  │
│  │  - User                                             │  │
│  │  - Exercise                                         │  │
│  │  - Plan / PlanWeek / TrainingSession               │  │
│  │  - Workout / ExerciseLog                            │  │
│  │  - Progress                                         │  │
│  │  - Medal                                            │  │
│  └─────────────────────────────────────────────────────┘  │
│                          ↕ SQL                              │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  Banco de Dados SQLite (evolua.db)                 │  │
│  │  - Persistência de dados                            │  │
│  │  - Relacionamentos entre entidades                  │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Camadas da Aplicação

### 1. Camada de Apresentação (Frontend)

**Arquivo:** `frontend/`

**Responsabilidades:**
- Interface do usuário responsiva
- Validação de formulários
- Comunicação com API via HTTP
- Gerenciamento de estado da aplicação
- Armazenamento local (localStorage)

**Componentes:**
- `index.html` - Estrutura HTML com modais e páginas
- `styles.css` - Estilos responsivos com CSS Grid/Flexbox
- `app.js` - Lógica da aplicação, navegação e handlers
- `api.js` - Cliente HTTP para comunicação com backend

**Stack:** HTML5, CSS3, JavaScript (Vanilla)

### 2. Camada de API (Backend)

**Arquivo:** `backend/app.py`

**Responsabilidades:**
- Exposição de endpoints RESTful
- Validação de dados
- Processamento de lógica de negócio
- Autenticação e autorização (futura)
- Tratamento de erros

**Endpoints Principais:**
- `/api/users` - CRUD de usuários
- `/api/exercises` - Gerenciamento de exercícios
- `/api/plans` - Criação de planos personalizados
- `/api/workouts` - Registro de treinos
- `/api/progress` - Acompanhamento de progresso
- `/api/medals` - Gerenciamento de medalhas

**Stack:** Python, Flask, Flask-CORS

### 3. Camada de Dados (Models & ORM)

**Arquivo:** `backend/models.py`

**Responsabilidades:**
- Definição de esquema de dados
- Relacionamentos entre entidades
- Validação em nível de model
- Mapeamento objeto-relacional

**Modelos:**

```
User
├── plans: List[Plan]
├── workouts: List[Workout]
├── progress: List[Progress]
└── medals: List[Medal]

Plan
├── weeks: List[PlanWeek]
└── user: User

PlanWeek
├── sessions: List[TrainingSession]
└── plan: Plan

TrainingSession
├── exercises: List[SessionExercise]
└── week: PlanWeek

SessionExercise
├── exercise: Exercise
└── session: TrainingSession

Exercise
├── sessions: List[SessionExercise]

Workout
├── exercises_log: List[ExerciseLog]
└── user: User

ExerciseLog
├── workout: Workout
├── exercise: Exercise

Progress
└── user: User

Medal
└── user: User
```

**Stack:** SQLAlchemy, SQLite

### 4. Camada de Configuração

**Arquivo:** `backend/config.py`

**Responsabilidades:**
- Gerenciar configurações por ambiente
- Variáveis de ambiente
- Configurações de banco de dados
- Chaves de segurança

**Ambientes:**
- Development
- Production
- Testing

## Fluxo de Dados

### Fluxo de Registro/Login

```
1. Frontend: Usuário preenche formulário
2. Frontend: app.js coleta dados do formulário
3. Frontend: api.js faz POST para /api/users
4. Backend: app.py recebe requisição
5. Backend: Valida dados
6. Backend: models.py cria novo User
7. Backend: Salva no banco de dados (SQLite)
8. Backend: Retorna dados do usuário em JSON
9. Frontend: Armazena userId no localStorage
10. Frontend: Redireciona para dashboard
```

### Fluxo de Registro de Treino

```
1. Frontend: Usuário preenche formulário de treino
2. Frontend: api.js faz POST para /api/workouts
3. Backend: app.py recebe requisição
4. Backend: Valida dados
5. Backend: models.py cria novo Workout
6. Backend: Calcula pontos (100 por treino)
7. Backend: Atualiza pontos do usuário
8. Backend: Salva no banco de dados
9. Backend: Retorna confirmação + pontos
10. Frontend: Exibe mensagem de sucesso
11. Frontend: Atualiza dashboard
```

### Fluxo de Criação de Plano

```
1. Frontend: Usuário clica "Criar Plano"
2. Frontend: api.js faz POST para /api/plans
3. Backend: app.py recebe user_id
4. Backend: Valida usuário existe
5. Backend: Cria Plan baseado no perfil do usuário
6. Backend: Cria PlanWeek para 4 semanas
7. Backend: Cria TrainingSession baseado em dias/semana
8. Backend: Salva tudo no banco de dados
9. Backend: Retorna detalhes do plano
10. Frontend: Exibe plano criado
```

## Modelo de Dados (ER Diagram)

```
┌──────────────┐
│    Users     │
├──────────────┤
│ id (PK)      │
│ name         │
│ email (UNIQUE)
│ password_hash│
│ age          │
│ objective    │
│ level        │
│ days_per_week│
│ training_loc │
│ points       │
│ created_at   │
└──────────────┘
      │ 1
      │
      ├─────────── N ─── ┌──────────────┐
      │                  │    Plans     │
      │                  ├──────────────┤
      │                  │ id (PK)      │
      │                  │ user_id (FK) │
      │                  │ name         │
      │                  │ description  │
      │                  │ duration_wks │
      │                  └──────────────┘
      │                         │ 1
      │                         │
      │                         └─ N ── ┌──────────────┐
      │                                  │ PlanWeeks    │
      │                                  ├──────────────┤
      │                                  │ id (PK)      │
      │                                  │ plan_id (FK) │
      │                                  │ week_number  │
      │                                  └──────────────┘
      │                                         │ 1
      │                                         │
      │                                         └─ N ── ┌─────────────────────┐
      │                                                  │ TrainingSessions    │
      │                                                  ├─────────────────────┤
      │                                                  │ id (PK)             │
      │                                                  │ plan_week_id (FK)   │
      │                                                  │ session_name        │
      │                                                  │ day_of_week         │
      │                                                  │ focus_group         │
      │                                                  └─────────────────────┘
      │                                                         │ 1
      │                                                         │
      │                                                         └─ N ── ┌────────────────────┐
      │                                                                  │ SessionExercises   │
      │                                                                  ├────────────────────┤
      │                                                                  │ id (PK)            │
      │                                                                  │ session_id (FK)    │
      │                                                                  │ exercise_id (FK)   │
      │                                                                  │ sets               │
      │                                                                  │ reps               │
      │                                                                  │ rest_seconds       │
      │                                                                  └────────────────────┘
      │
      │
      ├─────────── N ─── ┌──────────────┐
      │                  │   Workouts   │
      │                  ├──────────────┤
      │                  │ id (PK)      │
      │                  │ user_id (FK) │
      │                  │ date         │
      │                  │ duration_min │
      │                  │ total_weight │
      │                  │ calories     │
      │                  │ completed    │
      │                  └──────────────┘
      │                         │ 1
      │                         │
      │                         └─ N ── ┌──────────────┐
      │                                  │ ExerciseLogs │
      │                                  ├──────────────┤
      │                                  │ id (PK)      │
      │                                  │ workout_id   │
      │                                  │ exercise_id  │
      │                                  │ sets_done    │
      │                                  │ actual_reps  │
      │                                  │ weight_used  │
      │                                  │ difficulty   │
      │                                  └──────────────┘
      │
      │
      ├─────────── N ─── ┌──────────────┐
      │                  │  Progress    │
      │                  ├──────────────┤
      │                  │ id (PK)      │
      │                  │ user_id (FK) │
      │                  │ date         │
      │                  │ weight       │
      │                  │ measurements │
      │                  │ photo_url    │
      │                  │ notes        │
      │                  └──────────────┘
      │
      │
      └─────────── N ─── ┌──────────────┐
                         │   Medals     │
                         ├──────────────┤
                         │ id (PK)      │
                         │ user_id (FK) │
                         │ name         │
                         │ description  │
                         │ icon         │
                         │ earned_at    │
                         └──────────────┘


┌──────────────┐
│  Exercises   │
├──────────────┤
│ id (PK)      │
│ name (UNIQUE)│
│ muscle_group │
│ difficulty   │
│ description  │
│ instructions │
│ safety_tips  │
│ video_url    │
└──────────────┘
      │
      └─ N ── SessionExercises (relação M:N)
```

## Padrões de Projeto

### 1. MVC (Model-View-Controller)
- **Models:** `models.py` (banco de dados)
- **Views:** `index.html` (apresentação)
- **Controllers:** `app.py` (lógica)

### 2. RESTful API
- Endpoints seguem padrão REST
- Métodos HTTP (GET, POST, PUT, DELETE)
- Recursos bem definidos

### 3. Single Page Application (SPA)
- Navegação sem reload de página
- Estado gerenciado em JavaScript
- Requisições AJAX para API

## Segurança (Implementações Futuras)

- [ ] JWT para autenticação
- [ ] Hashing de senhas com bcrypt
- [ ] HTTPS/TLS
- [ ] CORS restritivo
- [ ] Rate limiting
- [ ] Validação de entrada
- [ ] SQL injection prevention (já usa ORM)
- [ ] XSS prevention

## Escalabilidade

**Melhorias para produção:**
- Trocar SQLite por PostgreSQL
- Adicionar Redis para caching
- Implementar autenticação JWT
- Load balancing com Nginx
- Docker containers
- CI/CD pipeline
- Monitoring e logging

## Estrutura de Arquivos Recomendada (Futuro)

```
evolua-app/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── exercise.py
│   │   │   ├── plan.py
│   │   │   └── ...
│   │   ├── routes/
│   │   │   ├── users.py
│   │   │   ├── exercises.py
│   │   │   ├── plans.py
│   │   │   └── ...
│   │   ├── services/
│   │   │   ├── user_service.py
│   │   │   ├── plan_service.py
│   │   │   └── ...
│   │   └── utils/
│   │       ├── validators.py
│   │       └── decorators.py
│   ├── tests/
│   ├── config.py
│   ├── wsgi.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── utils/
│   │   └── styles/
│   ├── public/
│   └── package.json
├── docs/
│   ├── API.md
│   ├── ARCHITECTURE.md
│   └── EXAMPLES.md
├── docker-compose.yml
├── .github/
│   └── workflows/
├── README.md
└── .gitignore
```

## Próximos Passos

1. **Autenticação:** Implementar JWT
2. **Banco de dados:** Migrar para PostgreSQL
3. **Cache:** Adicionar Redis
4. **Testing:** Escrever testes unitários e integração
5. **CI/CD:** GitHub Actions
6. **Docker:** Containerizar aplicação
7. **Monitoramento:** Implementar logs e alertas
8. **IA:** Integrar algoritmo para gerar planos
9. **Mobile:** Criar app React Native

---

Para mais detalhes, consulte a [documentação da API](API.md) e [exemplos de uso](EXAMPLES.md).
