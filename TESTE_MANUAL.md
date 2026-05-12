# EVOLUA MVP - Pronto para Testes 🚀

## ✅ O Que Foi Implementado

### Backend (Flask + SQLAlchemy + JWT)
- **Autenticação**: Registro, Login, JWT, Hash bcrypt
- **Modelos**: User, Plan, Exercise, Workout, Progress, Medal, etc
- **15+ Endpoints API** prontos:
  - `/api/auth/register` - Registrar
  - `/api/auth/login` - Login
  - `/api/users/profile` - Perfil (GET/PUT)
  - `/api/plans` - Planos (GET/POST)
  - `/api/plans/<id>` - Detalhes do plano
  - `/api/workouts` - Treinos (POST)
  - `/api/workouts/<id>/exercise` - Registrar exercício
  - `/api/workouts/<id>/complete` - Finalizar treino
  - `/api/medals/<user_id>` - Medalhas
  - `/api/stats/<user_id>` - Estatísticas
  - `/api/progress` - Registrar progresso
  - `/api/progress/<user_id>` - Histórico
  - `/api/exercises` - Listar exercícios

- **Gamificação**:
  - Sistema de pontos (10/exercício, 50/treino)
  - Medalhas automáticas (Primeira Semana, Dedicado, Campeão)
  - Streak tracker
  - Sistema de stats

### Frontend (HTML/CSS/JS Vanilla)
- **Páginas**:
  - Login/Register com validação
  - Dashboard com stats, planos e histórico
  - Tela de Treino com cronômetro
  - Progresso com gráfico de peso
  - Medalhas
  - Perfil do usuário

- **Design**:
  - Responsivo (Desktop, Tablet, Mobile)
  - Moderno com gradient
  - Animations e transições
  - Dark mode ready

### Banco de Dados
- SQLite (evolua.db)
- 9 tabelas normalizadas
- Relacionamentos com cascade
- Pronto para migração para PostgreSQL

### Dados Demo
- 8 exercícios padrão carregados
- Planos pré-configurados (A, B, C)
- Geração automática ao registro

---

## 🎯 Como Testar

### 1️⃣ **Setup Backend**

```bash
cd evolua-app/backend

# Criar ambiente virtual
python3 -m venv venv

# Ativar (Linux/Mac)
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Executar servidor
python3 app.py
```

✅ Backend rodando em `http://localhost:5000`

### 2️⃣ **Setup Frontend**

Abrir outro terminal:

```bash
cd evolua-app/frontend

# Servidor Python (Python 3)
python3 -m http.server 8000

# OU com Node.js
npm install -g http-server
http-server
```

✅ Frontend rodando em `http://localhost:8000`

### 3️⃣ **Testar via Interface Web**

1. Abrir `http://localhost:8000` no navegador
2. Clique em **"Criar Conta"**
3. Preencha:
   - Nome: João Silva
   - Email: joao@evolua.com
   - Senha: senha123
   - Objetivo: Ganho de Massa
   - Nível: Iniciante
4. Clique em **"Criar Conta"**

✅ Você será redirecionado para o Dashboard

### 4️⃣ **Explorar Funcionalidades**

**Dashboard:**
- Ver stats (Pontos, Treinos, Streak, Medalhas)
- Plano de treino será criado automaticamente
- Clique em "Ver Detalhes" para expandir

**Iniciar Treino:**
- Clique em "Iniciar Treino" em uma sessão
- Veja o cronômetro rodando
- Registre exercícios
- Clique em "Completo ✓" para cada exercício
- Finalize com "Finalizar Treino"

**Progresso:**
- Registre peso
- Veja gráfico de evolução

**Medalhas:**
- Veja medalhas conquistadas após completar treinos

### 5️⃣ **Testar API via cURL**

```bash
# 1. Registrar
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Teste User",
    "email": "teste@evolua.com",
    "password": "senha123",
    "objective": "hipertrofia",
    "level": "iniciante"
  }'

# Copie o access_token retornado

# 2. Usar token nos próximos requests
TOKEN="seu_token_aqui"

# Obter perfil
curl -X GET http://localhost:5000/api/users/profile \
  -H "Authorization: Bearer $TOKEN"

# Listar planos
curl -X GET http://localhost:5000/api/plans \
  -H "Authorization: Bearer $TOKEN"

# Listar exercícios
curl -X GET http://localhost:5000/api/exercises

# Obter stats
curl -X GET http://localhost:5000/api/stats/1 \
  -H "Authorization: Bearer $TOKEN"
```

### 6️⃣ **Testar com Script Python**

```bash
cd evolua-app

# Instalar requests
pip install requests

# Executar testes
python3 test_api.py
```

Isso vai:
- Criar usuário
- Login
- Criar plano
- Registrar treino
- Mostrar stats e medalhas

---

## 📊 Fluxo de Usuário Completo

```
1. Registro
   ↓
2. Perfil criado (objetivo, nível, local)
   ↓
3. Plano de treino gerado automaticamente
   ↓
4. Dashboard com stats
   ↓
5. Iniciar Treino (Treino A, B ou C)
   ↓
6. Executar exercícios com vídeos
   ↓
7. Registrar séries, reps, peso
   ↓
8. Finalizar treino → +50 pontos
   ↓
9. Verificar medalhas (se aplicável)
   ↓
10. Registrar progresso (peso, medidas)
   ↓
11. Ver gráficos de evolução
```

---

## 🔍 O Que Testar

### ✅ Autenticação
- [ ] Registrar novo usuário
- [ ] Login com credenciais
- [ ] Token JWT sendo salvo
- [ ] Erro ao login com senha errada

### ✅ Planos
- [ ] Plano criado automaticamente após registro
- [ ] Plano tem 3 sessões (A, B, C)
- [ ] Cada sessão tem exercícios
- [ ] Detalhes do plano mostram tudo

### ✅ Treino
- [ ] Iniciar treino começa cronômetro
- [ ] Registrar exercício funciona
- [ ] Finalizar treino calcula duração
- [ ] Pontos adicionados ao usuário

### ✅ Gamificação
- [ ] Primeiro treino = Medalha "Primeira Semana"
- [ ] Stats aparecem no dashboard
- [ ] Streak está contando dias

### ✅ Progresso
- [ ] Registrar peso funciona
- [ ] Gráfico de peso aparece
- [ ] Histórico mostra registros

### ✅ Responsividade
- [ ] Desktop looks bom
- [ ] Tablet se adapta
- [ ] Mobile navega bem

---

## 📁 Estrutura de Arquivos

```
evolua-app/
├── backend/
│   ├── app.py                 ← API principal (22.5 KB)
│   ├── models.py              ← Modelos SQLAlchemy
│   ├── config.py              ← Configurações
│   ├── requirements.txt        ← Dependências
│   ├── .env                    ← Variáveis ambiente
│   └── venv/                   ← Ambiente virtual
│
├── frontend/
│   ├── index.html             ← HTML
│   ├── app.js                 ← App SPA (29 KB)
│   ├── api.js                 ← Cliente API (4.7 KB)
│   └── styles.css             ← Estilos (11 KB)
│
├── test_api.py                ← Script de testes
├── SETUP_GUIDE.md             ← Guia detalhado
└── README.md                  ← Este arquivo
```

---

## 🐛 Possíveis Issues & Soluções

### Backend não conecta
```bash
# Verificar porta
sudo lsof -i :5000

# Matar processo
lsof -ti:5000 | xargs kill -9
```

### CORS error
```javascript
// Já está configurado em app.py
// Se ainda tiver problema:
FLASK_ENV=development python3 app.py
```

### Banco de dados corrompido
```bash
rm evolua.db
python3 -c "from app import db; db.create_all()"
```

### Frontend não carrega API
```bash
# Verificar se backend está rodando
curl http://localhost:5000/health

# Verificar console do navegador (F12)
# Deve mostrar requisições HTTP
```

---

## 🎓 Aprendizados Implementados

✅ **Autenticação JWT** - Segura, stateless, produção-ready
✅ **Hashing de Senha** - bcrypt para segurança
✅ **API RESTful** - Endpoints bem estruturados
✅ **SPA Frontend** - Sem reload, rápido
✅ **Responsividade** - Mobile-first CSS
✅ **Gamificação** - Sistema de pontos e medalhas
✅ **Banco de Dados** - Modelos normalizados
✅ **Tratamento de Erros** - Status codes HTTP apropriados

---

## 🚀 Próximas Melhorias

1. **Teste Unitário**: Adicionar pytest no backend
2. **React Native**: Aplicativo mobile nativo
3. **IA Real**: Integrar modelo de ML para adaptação
4. **Banco PostgreSQL**: Para produção
5. **Docker**: Containerizar tudo
6. **CI/CD**: GitHub Actions para testes
7. **Dashboard Admin**: Gerenciar usuários e exercícios
8. **Push Notifications**: Lembretes de treino

---

## 📞 Dúvidas?

Se tiver qualquer dúvida durante os testes, todos os endpoints estão documentados em `SETUP_GUIDE.md`.

---

**EVOLUA MVP - Seu Personal Trainer Digital 🏋️💪**

Pronto para transformar vidas! 🚀
