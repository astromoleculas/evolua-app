# Documentação da API Evolua

## Introdução

A API Evolua fornece endpoints RESTful para gerenciar usuários, planos de treino, exercícios, treinos registrados e progresso.

**Base URL:** `http://localhost:5000/api`

## Autenticação

Atualmente, a API não requer autenticação. Em produção, será implementada autenticação JWT.

## Formatos

Todas as requisições e respostas usam JSON.

## Endpoints

### Users (Usuários)

#### Criar Usuário
```
POST /users
```

**Request:**
```json
{
  "name": "João Silva",
  "email": "joao@example.com",
  "password": "senha123",
  "age": 25,
  "objective": "ganho_massa",
  "level": "iniciante",
  "days_per_week": 3,
  "training_location": "academia"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "name": "João Silva",
  "email": "joao@example.com",
  "objective": "ganho_massa",
  "level": "iniciante",
  "points": 0
}
```

#### Obter Usuário
```
GET /users/<user_id>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "João Silva",
  "email": "joao@example.com",
  "age": 25,
  "objective": "ganho_massa",
  "level": "iniciante",
  "days_per_week": 3,
  "training_location": "academia",
  "points": 150,
  "created_at": "2025-01-15T10:30:00"
}
```

#### Atualizar Usuário
```
PUT /users/<user_id>
```

**Request:**
```json
{
  "name": "João Silva Atualizado",
  "age": 26,
  "objective": "perda_peso"
}
```

**Response (200 OK):**
```json
{
  "message": "User updated successfully"
}
```

### Exercises (Exercícios)

#### Listar Exercícios
```
GET /exercises
GET /exercises?muscle_group=Peito
GET /exercises?difficulty=Iniciante
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Supino Reto",
    "muscle_group": "Peito",
    "difficulty": "Intermediario",
    "description": "Exercício para desenvolvimento do peito",
    "instructions": "Deite-se no banco...",
    "safety_tips": "Mantenha os cotovelos...",
    "video_url": "https://example.com/video.mp4"
  }
]
```

#### Criar Exercício
```
POST /exercises
```

**Request:**
```json
{
  "name": "Supino Reto com Halteres",
  "muscle_group": "Peito",
  "difficulty": "Intermediario",
  "description": "Exercício para desenvolvimento do peito",
  "instructions": "Deite-se no banco com pés no chão...",
  "safety_tips": "Evite carregar muito peso...",
  "video_url": "https://example.com/video.mp4"
}
```

**Response (201 Created):**
```json
{
  "id": 5,
  "name": "Supino Reto com Halteres",
  "muscle_group": "Peito"
}
```

### Plans (Planos de Treino)

#### Criar Plano
```
POST /plans
```

**Request:**
```json
{
  "user_id": 1
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "name": "Plano ganho_massa - iniciante",
  "description": "Plano personalizado de 3 dias por semana",
  "duration_weeks": 12
}
```

#### Obter Plano
```
GET /plans/<plan_id>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Plano ganho_massa - iniciante",
  "description": "Plano personalizado de 3 dias por semana",
  "duration_weeks": 12,
  "created_at": "2025-01-15T10:30:00",
  "weeks": [
    {
      "week_number": 1,
      "sessions": [
        {
          "id": 1,
          "name": "Treino A",
          "focus": "Peito e Tríceps",
          "day": 1
        }
      ]
    }
  ]
}
```

### Workouts (Treinos)

#### Registrar Treino
```
POST /workouts
```

**Request:**
```json
{
  "user_id": 1,
  "training_session_id": 1,
  "duration_minutes": 60,
  "total_weight": 500.5,
  "calories_burned": 350.0,
  "completed": true,
  "notes": "Treino muito bom, senti bastante cansaço"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "points_earned": 100,
  "total_points": 250
}
```

#### Obter Treinos do Usuário
```
GET /workouts/<user_id>
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "date": "2025-01-15T14:30:00",
    "duration_minutes": 60,
    "total_weight": 500.5,
    "calories_burned": 350.0,
    "completed": true
  },
  {
    "id": 2,
    "date": "2025-01-13T14:00:00",
    "duration_minutes": 55,
    "total_weight": 480.0,
    "calories_burned": 320.0,
    "completed": true
  }
]
```

### Progress (Progresso)

#### Registrar Progresso
```
POST /progress
```

**Request:**
```json
{
  "user_id": 1,
  "weight": 75.5,
  "body_measurements": {
    "chest": 100,
    "waist": 80,
    "arm": 32
  },
  "photo_url": "https://example.com/photo.jpg",
  "notes": "Começando a ver mudanças"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "date": "2025-01-15T14:30:00"
}
```

#### Obter Histórico de Progresso
```
GET /progress/<user_id>
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "date": "2025-01-15T14:30:00",
    "weight": 75.5,
    "measurements": {
      "chest": 100,
      "waist": 80,
      "arm": 32
    },
    "photo_url": "https://example.com/photo.jpg",
    "notes": "Começando a ver mudanças"
  }
]
```

### Medals (Medalhas)

#### Obter Medalhas do Usuário
```
GET /medals/<user_id>
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Primeira Semana",
    "icon": "bronze",
    "earned_at": "2025-01-15T14:30:00"
  },
  {
    "id": 2,
    "name": "Mês Completo",
    "icon": "silver",
    "earned_at": "2025-02-15T14:30:00"
  }
]
```

#### Atribuir Medalha
```
POST /medals
```

**Request:**
```json
{
  "user_id": 1,
  "name": "Primeira Semana",
  "description": "Completou sua primeira semana de treinos",
  "icon": "bronze"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "name": "Primeira Semana"
}
```

## Health Check

#### Verificar Status da API
```
GET /health
```

**Response (200 OK):**
```json
{
  "status": "ok",
  "message": "Evolua API running"
}
```

## Códigos de Status HTTP

| Código | Significado |
|--------|-------------|
| 200 | OK - Requisição bem-sucedida |
| 201 | Created - Recurso criado com sucesso |
| 400 | Bad Request - Requisição inválida |
| 404 | Not Found - Recurso não encontrado |
| 409 | Conflict - Email já existe |
| 500 | Internal Server Error - Erro interno do servidor |

## Exemplos com cURL

### Criar Usuário
```bash
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Silva",
    "email": "joao@example.com",
    "password": "senha123",
    "age": 25,
    "objective": "ganho_massa",
    "level": "iniciante",
    "days_per_week": 3,
    "training_location": "academia"
  }'
```

### Obter Usuário
```bash
curl http://localhost:5000/api/users/1
```

### Registrar Treino
```bash
curl -X POST http://localhost:5000/api/workouts \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "duration_minutes": 60,
    "total_weight": 500,
    "calories_burned": 350,
    "completed": true,
    "notes": "Treino ótimo"
  }'
```

## Tratamento de Erros

Todos os erros retornam um JSON com a seguinte estrutura:

```json
{
  "error": "Descrição do erro"
}
```

Exemplos:
```json
{
  "error": "User not found"
}
```

```json
{
  "error": "Email already exists"
}
```

```json
{
  "error": "Missing required fields"
}
```

## Futuras Melhorias

- [ ] Autenticação JWT
- [ ] Rate limiting
- [ ] Paginação de resultados
- [ ] Filtros avançados
- [ ] Caching com Redis
- [ ] Webhooks
- [ ] Documentação OpenAPI/Swagger
