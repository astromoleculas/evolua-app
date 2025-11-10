# Guia Rápido - Evolua

Comece a usar o Evolua em 5 minutos!

## 1. Instalar e Executar o Backend

```bash
cd backend

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Executar servidor
python app.py
```

O backend estará em `http://localhost:5000`

## 2. Executar o Frontend

Em outro terminal:

```bash
cd frontend

# Executar servidor web (Python 3)
python -m http.server 8000
```

O frontend estará em `http://localhost:8000`

## 3. Usar a Aplicação

1. Abra `http://localhost:8000` no navegador
2. Faça login (crie uma conta)
3. Complete seu perfil
4. Comece a registrar treinos!

## Estrutura de Pastas

```
evolua-app/
├── backend/          # API Flask
│   ├── app.py       # Aplicação principal
│   ├── models.py    # Modelos de dados
│   ├── config.py    # Configurações
│   ├── seed.py      # Popular banco com exemplos
│   └── requirements.txt
├── frontend/         # Interface web
│   ├── index.html
│   ├── styles.css
│   ├── app.js
│   └── api.js
├── docs/             # Documentação
│   └── API.md
└── README.md
```

## Dados de Teste

Para adicionar exercícios de exemplo ao banco:

```bash
cd backend
python seed.py
```

## API Endpoints Principais

```
POST   /api/users                    # Criar usuário
GET    /api/users/<id>              # Obter usuário
PUT    /api/users/<id>              # Atualizar usuário

POST   /api/workouts                # Registrar treino
GET    /api/workouts/<user_id>      # Obter treinos

POST   /api/progress                # Registrar progresso
GET    /api/progress/<user_id>      # Obter progresso

GET    /api/exercises               # Listar exercícios
POST   /api/exercises               # Criar exercício
```

## Solução de Problemas

### Port 5000 já está em uso
```bash
python app.py --port 5001
```

### Port 8000 já está em uso
```bash
python -m http.server 9000
```

### CORS error
Certifique-se de que o backend está rodando em `http://localhost:5000`

### Banco de dados vazio
```bash
cd backend
python seed.py
```

## Próximos Passos

1. Explore o dashboard
2. Crie seu perfil
3. Registre seus primeiros treinos
4. Acompanhe seu progresso
5. Ganhe medalhas e pontos!

## Documentação Completa

Veja [README.md](README.md) e [docs/API.md](docs/API.md) para mais detalhes.

---

Divirta-se com o Evolua! 💪
