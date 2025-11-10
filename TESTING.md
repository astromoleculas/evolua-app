# Guia de Testes - Evolua

Tudo que você precisa saber para testar a aplicação Evolua com dados reais.

## 1️⃣ Instalar Dependências

```bash
cd backend
pip install -r requirements.txt
```

## 2️⃣ Popular Banco de Dados com Dados de Teste

Execute o script que popula o banco de dados com 3 usuários, 42 treinos, 12 registros de progresso e 11 medalhas:

```bash
python mock_data.py
```

**Output esperado:**
```
==================================================
Populando banco de dados com dados de teste
==================================================

✓ Banco de dados limpo
✓ 17 exercícios adicionados
✓ 3 usuários adicionados
✓ 3 planos e sessões adicionados
✓ 42 treinos adicionados
✓ 12 registros de progresso adicionados
✓ 11 medalhas adicionadas
```

## 3️⃣ Iniciar Backend

Em um terminal:

```bash
cd backend
python app.py
```

Acesse: http://localhost:5000/api/health

## 4️⃣ Iniciar Frontend

Em outro terminal:

```bash
cd frontend
python -m http.server 8000
```

Acesse: http://localhost:8000

## 📝 Usuários de Teste

### 👨 Carlos Mendes (Iniciante)
- **Email:** `carlos@example.com`
- **Objetivo:** Ganho de Massa
- **Nível:** Iniciante
- **Dias:** 3 dias/semana
- **Local:** Academia
- **Dados:**
  - 14 treinos registrados
  - 4 registros de progresso
  - 3 medalhas conquistadas
  - 450 pontos

### 👩 Juliana Lima (Intermediária)
- **Email:** `juliana@example.com`
- **Objetivo:** Perda de Peso
- **Nível:** Intermediário
- **Dias:** 4 dias/semana
- **Local:** Casa
- **Dados:**
  - 14 treinos registrados
  - 4 registros de progresso (com perda de peso)
  - 4 medalhas conquistadas
  - 750 pontos

### 👨‍💼 João Silva (Avançado)
- **Email:** `joao@example.com`
- **Objetivo:** Tonificação
- **Nível:** Intermediário
- **Dias:** 5 dias/semana
- **Local:** Academia
- **Dados:**
  - 14 treinos registrados
  - 4 registros de progresso
  - 3 medalhas conquistadas
  - 600 pontos

## 🧪 Cenários de Teste

### Teste 1: Dashboard
1. Login como `carlos@example.com`
2. Veja o dashboard com:
   - 450 pontos
   - 14 treinos completos
   - 3 medalhas
   - Últimos treinos listados

### Teste 2: Perfil
1. Vá para "Perfil"
2. Veja os dados preenchidos (21 anos, ganho de massa, iniciante)
3. Mude a idade para 22
4. Clique "Salvar Perfil"
5. Recarregue a página, idade deve ser 22

### Teste 3: Planos
1. Vá para "Planos"
2. Veja 1 plano criado
3. Clique "Ver Detalhes"
4. Veja as 4 semanas de treino
5. Clique "Deletar" e confirme
6. Clique "Criar Novo Plano"
7. Veja o novo plano aparecer

### Teste 4: Treinos
1. Vá para "Treinos"
2. Veja 14 treinos dos últimos 30 dias
3. Clique "Registrar Treino"
4. Preencha:
   - Duração: 50 minutos
   - Peso: 350 kg
   - Calorias: 280
5. Clique "Registrar Treino"
6. Novo treino deve aparecer no topo
7. Pontos devem aumentar de 450 para 550

### Teste 5: Progresso
1. Vá para "Evolução"
2. Veja 4 registros de progresso
3. Para Juliana: veja perda de peso progressiva (80 → 78,5 → 77 → 75,5)
4. Clique "Registrar Progresso"
5. Preencha:
   - Peso: 75.0 kg
   - Notas: "Estou vendo resultados!"
6. Novo registro deve aparecer

### Teste 6: Comparativo entre Usuários
1. Login como Carlos (3 dias/semana)
2. Veja plano com 3 sessões
3. Logout
4. Login como Juliana (4 dias/semana)
5. Veja plano com 4 sessões
6. Observe como o plano é personalizado

### Teste 7: Medalhas
1. Login como Juliana (4 medalhas)
2. Dashboard mostra 4 medalhas
3. Login como Carlos (3 medalhas)
4. Dashboard mostra 3 medalhas

## 🔍 Verificações Técnicas

### Backend
```bash
# Health check
curl http://localhost:5000/api/health

# Listar usuários (verificar dados)
curl http://localhost:5000/api/users/1

# Listar treinos de usuário
curl http://localhost:5000/api/workouts/1

# Listar planos de usuário
curl http://localhost:5000/api/plans/user/1

# Listar progresso de usuário
curl http://localhost:5000/api/progress/1
```

### Banco de Dados
```bash
# Visualizar quantos registros existem
sqlite3 backend/evolua.db "SELECT COUNT(*) FROM users;"
sqlite3 backend/evolua.db "SELECT COUNT(*) FROM workouts;"
sqlite3 backend/evolua.db "SELECT COUNT(*) FROM progress;"
```

## 🐛 Troubleshooting

### "Banco de dados vazio"
```bash
cd backend
python mock_data.py
```

### "Connection refused"
- Certifique-se que o backend está rodando em outro terminal
- Acesse http://localhost:5000/api/health para confirmar

### "Dados não aparecem"
- Abra o console do navegador (F12)
- Veja se há erros na aba Console
- Verifique a aba Network para requisições

### "Quero resetar os dados"
```bash
cd backend
python mock_data.py  # Limpa e popula tudo novamente
```

## 📊 Estrutura de Dados Criada

### Usuários: 3
### Exercícios: 17
### Planos: 3 (1 por usuário)
### Semanas de Treino: 12 (4 por plano)
### Sessões de Treino: 36+ (3-5 por semana)
### Treinos Registrados: 42 (14 por usuário)
### Registros de Progresso: 12 (4 por usuário)
### Medalhas: 11 (3-4 por usuário)
### Total de Registros: 130+

## ✅ Funcionalidades Testáveis

- ✅ Login/Registro (sem validação de senha)
- ✅ Visualizar Dashboard
- ✅ Editar Perfil
- ✅ Criar Plano de Treino
- ✅ Deletar Plano
- ✅ Ver Detalhes do Plano
- ✅ Registrar Treino
- ✅ Ver Histórico de Treinos
- ✅ Registrar Progresso
- ✅ Ver Evolução (múltiplos registros)
- ✅ Ver Medalhas Conquistadas
- ✅ Ganhar Pontos (100 por treino)

## 🎯 Fluxo de Teste Completo

1. **Frontend aberto** em http://localhost:8000
2. **Login** com `carlos@example.com`
3. **Dashboard** mostra 450 pontos e 14 treinos
4. **Perfil** mostra dados pessoais (21 anos, ganho de massa)
5. **Planos** mostra 1 plano criado
6. **Treinos** mostra 14 treinos dos últimos 30 dias
7. **Evolução** mostra 4 registros de progresso
8. **Registrar Treino** adiciona novo treino e aumenta pontos
9. **Logout e Login** como Juliana para ver dados diferentes

---

**Tempo estimado de teste completo:** 15 minutos

Para mais informações, veja [docs/TEST_DATA.md](docs/TEST_DATA.md)
