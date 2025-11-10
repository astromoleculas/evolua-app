# Exemplos de Uso da API Evolua

## Registrar e Login do Usuário

### 1. Criar um novo usuário (registro)

```bash
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Carlos Mendes",
    "email": "carlos@example.com",
    "password": "senha123",
    "age": 21,
    "objective": "ganho_massa",
    "level": "iniciante",
    "days_per_week": 3,
    "training_location": "academia"
  }'
```

**Resposta:**
```json
{
  "id": 1,
  "name": "Carlos Mendes",
  "email": "carlos@example.com",
  "objective": "ganho_massa",
  "level": "iniciante",
  "points": 0
}
```

### 2. Obter dados do usuário

```bash
curl http://localhost:5000/api/users/1
```

**Resposta:**
```json
{
  "id": 1,
  "name": "Carlos Mendes",
  "email": "carlos@example.com",
  "age": 21,
  "objective": "ganho_massa",
  "level": "iniciante",
  "days_per_week": 3,
  "training_location": "academia",
  "points": 100,
  "created_at": "2025-01-15T10:30:00"
}
```

### 3. Atualizar perfil do usuário

```bash
curl -X PUT http://localhost:5000/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{
    "age": 22,
    "objective": "tonificacao",
    "days_per_week": 4
  }'
```

**Resposta:**
```json
{
  "message": "User updated successfully"
}
```

## Criar Plano de Treino

### 4. Criar um plano personalizado

```bash
curl -X POST http://localhost:5000/api/plans \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1
  }'
```

**Resposta:**
```json
{
  "id": 1,
  "name": "Plano ganho_massa - iniciante",
  "description": "Plano personalizado de 3 dias por semana",
  "duration_weeks": 12
}
```

### 5. Obter detalhes do plano

```bash
curl http://localhost:5000/api/plans/1
```

**Resposta:**
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
          "focus": "Grupo A",
          "day": 0
        },
        {
          "id": 2,
          "name": "Treino B",
          "focus": "Grupo B",
          "day": 2
        },
        {
          "id": 3,
          "name": "Treino C",
          "focus": "Grupo C",
          "day": 4
        }
      ]
    }
  ]
}
```

## Gerenciar Exercícios

### 6. Listar todos os exercícios

```bash
curl http://localhost:5000/api/exercises
```

### 7. Filtrar exercícios por grupo muscular

```bash
curl "http://localhost:5000/api/exercises?muscle_group=Peito"
```

### 8. Filtrar exercícios por dificuldade

```bash
curl "http://localhost:5000/api/exercises?difficulty=Iniciante"
```

**Resposta:**
```json
[
  {
    "id": 2,
    "name": "Flexão no Banco",
    "muscle_group": "Peito",
    "difficulty": "Iniciante",
    "description": "Variante mais fácil da flexão tradicional",
    "instructions": "1. Coloque as mãos no banco...",
    "safety_tips": "Mantenha o corpo reto...",
    "video_url": "https://example.com/video.mp4"
  }
]
```

### 9. Criar um novo exercício

```bash
curl -X POST http://localhost:5000/api/exercises \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Prancha",
    "muscle_group": "Abdômen",
    "difficulty": "Iniciante",
    "description": "Exercício isométrico para core",
    "instructions": "1. Deite-se de bruços...",
    "safety_tips": "Mantenha o corpo alinhado...",
    "video_url": "https://example.com/prancha.mp4"
  }'
```

**Resposta:**
```json
{
  "id": 15,
  "name": "Prancha",
  "muscle_group": "Abdômen"
}
```

## Registrar Treinos

### 10. Registrar um treino concluído

```bash
curl -X POST http://localhost:5000/api/workouts \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "training_session_id": 1,
    "duration_minutes": 60,
    "total_weight": 500.5,
    "calories_burned": 350.0,
    "completed": true,
    "notes": "Treino muito bom, senti bastante cansaço"
  }'
```

**Resposta:**
```json
{
  "id": 1,
  "points_earned": 100,
  "total_points": 100
}
```

### 11. Obter histórico de treinos do usuário

```bash
curl http://localhost:5000/api/workouts/1
```

**Resposta:**
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

## Registrar Progresso

### 12. Registrar progresso (peso e fotos)

```bash
curl -X POST http://localhost:5000/api/progress \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "weight": 75.5,
    "body_measurements": {
      "chest": 100,
      "waist": 80,
      "arm": 32
    },
    "photo_url": "https://example.com/photo-2025-01-15.jpg",
    "notes": "Começando a ver mudanças no peito"
  }'
```

**Resposta:**
```json
{
  "id": 1,
  "date": "2025-01-15T14:30:00"
}
```

### 13. Obter histórico de progresso

```bash
curl http://localhost:5000/api/progress/1
```

**Resposta:**
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
    "photo_url": "https://example.com/photo-2025-01-15.jpg",
    "notes": "Começando a ver mudanças"
  }
]
```

## Gerenciar Medalhas

### 14. Obter medalhas do usuário

```bash
curl http://localhost:5000/api/medals/1
```

**Resposta:**
```json
[
  {
    "id": 1,
    "name": "Primeira Semana",
    "icon": "bronze",
    "earned_at": "2025-01-15T14:30:00"
  }
]
```

### 15. Atribuir medalha ao usuário

```bash
curl -X POST http://localhost:5000/api/medals \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "name": "Primeira Semana",
    "description": "Completou sua primeira semana de treinos",
    "icon": "bronze"
  }'
```

**Resposta:**
```json
{
  "id": 1,
  "name": "Primeira Semana"
}
```

## Verificar Status da API

### 16. Health check

```bash
curl http://localhost:5000/api/health
```

**Resposta:**
```json
{
  "status": "ok",
  "message": "Evolua API running"
}
```

## Fluxo Completo - Exemplo Prático

1. **Criar usuário** (Ex. 1)
2. **Criar plano de treino** (Ex. 4)
3. **Visualizar exercícios** (Ex. 6-8)
4. **Registrar primeiro treino** (Ex. 10)
5. **Registrar progresso** (Ex. 12)
6. **Ver medalhas conquistadas** (Ex. 14)

## Usando com JavaScript/Fetch API

```javascript
// Criar usuário
const response = await fetch('http://localhost:5000/api/users', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'João Silva',
    email: 'joao@example.com',
    password: 'senha123',
    age: 25,
    objective: 'ganho_massa',
    level: 'iniciante',
    days_per_week: 3,
    training_location: 'academia'
  })
});

const user = await response.json();
console.log('Usuário criado:', user);

// Registrar treino
const workoutResponse = await fetch('http://localhost:5000/api/workouts', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    user_id: user.id,
    duration_minutes: 60,
    total_weight: 500,
    calories_burned: 350,
    completed: true,
    notes: 'Ótimo treino!'
  })
});

const workout = await workoutResponse.json();
console.log('Treino registrado:', workout);
```

## Usando com Python/Requests

```python
import requests

BASE_URL = 'http://localhost:5000/api'

# Criar usuário
user_data = {
    'name': 'Maria Silva',
    'email': 'maria@example.com',
    'password': 'senha123',
    'age': 28,
    'objective': 'perda_peso',
    'level': 'intermediario',
    'days_per_week': 4,
    'training_location': 'casa'
}

response = requests.post(f'{BASE_URL}/users', json=user_data)
user = response.json()
print(f"Usuário criado: {user}")

# Registrar treino
workout_data = {
    'user_id': user['id'],
    'duration_minutes': 45,
    'total_weight': 300,
    'calories_burned': 280,
    'completed': True,
    'notes': 'Treino em casa'
}

response = requests.post(f'{BASE_URL}/workouts', json=workout_data)
workout = response.json()
print(f"Treino registrado: {workout}")
```

---

Para mais detalhes, veja a [documentação completa da API](API.md)
