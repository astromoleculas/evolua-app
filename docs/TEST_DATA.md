# Dados de Teste - Evolua

Este documento descreve os dados de teste disponíveis para testar a aplicação Evolua.

## Como Popular o Banco de Dados

### 1. Limpar e Popular com Dados de Teste

```bash
cd backend
python mock_data.py
```

Este script irá:
- Limpar o banco de dados anterior
- Criar 3 usuários de teste
- Criar 15+ exercícios de exemplo
- Criar planos de treino para cada usuário
- Gerar 14 treinos registrados por usuário
- Adicionar registros de progresso (peso e fotos)
- Atribuir medalhas conquistadas
- Calcular pontos automaticamente

### 2. Apenas Adicionar Exercícios (sem limpar dados)

```bash
cd backend
python seed.py
```

## Usuários de Teste

### 1. Carlos Mendes (Iniciante)
- **Email:** `carlos@example.com`
- **Senha:** `senha123` (qualquer uma funciona, é apenas para referência)
- **Objetivo:** Ganho de Massa
- **Nível:** Iniciante
- **Dias de Treino:** 3 dias/semana
- **Local:** Academia
- **Pontos:** 450
- **Perfil:** Estudante de 21 anos, iniciante que começou há um mês

**Dados Disponíveis:**
- ✅ Plano de treino criado
- ✅ 14 treinos registrados (últimos 30 dias)
- ✅ 4 registros de progresso
- ✅ 3 medalhas conquistadas

---

### 2. Juliana Lima (Intermediária)
- **Email:** `juliana@example.com`
- **Senha:** `senha456` (qualquer uma funciona, é apenas para referência)
- **Objetivo:** Perda de Peso
- **Nível:** Intermediário
- **Dias de Treino:** 4 dias/semana
- **Local:** Casa
- **Pontos:** 750
- **Perfil:** Gerente de 34 anos, retornando aos treinos

**Dados Disponíveis:**
- ✅ Plano de treino criado
- ✅ 14 treinos registrados (últimos 30 dias)
- ✅ 4 registros de progresso (com perda de peso)
- ✅ 4 medalhas conquistadas

---

### 3. João Silva (Intermediário/Avançado)
- **Email:** `joao@example.com`
- **Senha:** `senha789` (qualquer uma funciona, é apenas para referência)
- **Objetivo:** Tonificação
- **Nível:** Intermediário
- **Dias de Treino:** 5 dias/semana
- **Local:** Academia
- **Pontos:** 600
- **Perfil:** Profissional de 28 anos, consistente nos treinos

**Dados Disponíveis:**
- ✅ Plano de treino criado
- ✅ 14 treinos registrados (últimos 30 dias)
- ✅ 4 registros de progresso
- ✅ 3 medalhas conquistadas

---

## Exercícios Disponíveis

Total de **17 exercícios** agrupados por grupo muscular:

### Peito (3 exercícios)
- Supino Reto com Halteres (Intermediário)
- Flexão no Banco (Iniciante)
- Supino Inclinado (Intermediário)

### Costas (3 exercícios)
- Puxada Frontal (Intermediário)
- Remada Inclinada (Intermediário)
- Barra Fixa (Avançado)

### Perna (3 exercícios)
- Supino para Pernas (Iniciante)
- Agachamento com Peso (Avançado)
- Legpress (Intermediário)
- Rosca Direta de Pernas (Iniciante)

### Braço (4 exercícios)
- Rosca Direta (Iniciante)
- Rosca Inversa (Intermediário)
- Extensão de Tríceps (Iniciante)
- Rosca Concentrada (Intermediário)

### Ombro (3 exercícios)
- Desenvolvimento com Halteres (Intermediário)
- Elevação Lateral (Iniciante)
- Encolhimento de Ombros (Iniciante)

---

## Estrutura de Dados de Teste

### Planos de Treino
- **3 planos** - um para cada usuário
- **4 semanas** de treino em cada plano
- **3-5 sessões** de treino por semana (baseado no perfil do usuário)
- Cada sessão tem um foco muscular diferente

Exemplo de Plano (Carlos - 3 dias/semana):
```
Semana 1
├── Treino A (Segunda) - Peito e Tríceps
├── Treino B (Quarta) - Costas e Bíceps
└── Treino C (Sexta) - Perna
```

### Treinos Registrados
- **42 treinos** no total (14 por usuário)
- **Distribuídos nos últimos 30 dias**
- Cada treino tem:
  - Data e duração (45-75 minutos)
  - Peso total levantado (200-480 kg)
  - Calorias queimadas (300-450 kcal)
  - Notas descritivas

### Progresso Registrado
- **12 registros** de progresso (4 por usuário)
- **Mensais** (a cada 7 dias)
- Cada registro inclui:
  - Peso corporal
  - Medidas (peito, cintura, braço, coxa)
  - URL de foto (simulada)
  - Notas de progresso

**Progressão de Juliana (Perda de Peso):**
```
Semana 0: 80 kg
Semana 1: 78.5 kg
Semana 2: 77.0 kg
Semana 3: 75.5 kg
```

### Medalhas Conquistadas
- **10 medalhas** no total
- Tipos:
  - 🥉 **Bronze:** Primeira Semana
  - 🥈 **Silver:** Mês Completo
  - 🥇 **Gold:** Persistência de Aço (30 treinos)
  - 💎 **Platinum:** Rei do Treino (50 treinos)

---

## Fluxo de Teste Recomendado

### 1. Teste de Login
```
1. Abra http://localhost:8000
2. Use qualquer um dos emails de teste
3. Use qualquer senha (o sistema não valida ainda)
4. Você será logado e verá o dashboard
```

### 2. Teste do Dashboard
```
1. Veja os pontos totais (450-750)
2. Veja o número de treinos (14)
3. Veja o número de medalhas (3-4)
4. Veja os últimos treinos listados
```

### 3. Teste de Perfil
```
1. Vá para "Perfil"
2. Veja seus dados preenchidos
3. Edite algum campo
4. Clique "Salvar Perfil"
5. Os dados devem ser atualizados
```

### 4. Teste de Planos
```
1. Vá para "Planos"
2. Veja o plano criado
3. Clique "Ver Detalhes"
4. Clique "Deletar" e confirme
5. O plano deve ser removido
6. Clique "Criar Novo Plano"
7. Um novo plano deve aparecer
```

### 5. Teste de Treinos
```
1. Vá para "Treinos"
2. Veja os 14 treinos registrados
3. Clique "Registrar Treino"
4. Preencha os campos
5. Clique "Registrar Treino"
6. Novo treino deve aparecer na lista
7. Seus pontos devem aumentar em 100
```

### 6. Teste de Progresso
```
1. Vá para "Evolução"
2. Veja os 4 registros de progresso anteriores
3. Clique "Registrar Progresso"
4. Preencha peso e outros dados
5. Novo registro deve aparecer
6. Gráficos devem ser atualizados
```

### 7. Teste Comparativo (Carlos vs Juliana vs João)
```
1. Faça login como Carlos
2. Anote os dados (objetivo, nível, plano)
3. Faça logout
4. Faça login como Juliana
5. Compare os dados diferentes
6. Observe como os planos são diferentes baseado no perfil
```

---

## Dicas para Testes Adicionais

### Criar Múltiplos Planos
1. Vá para "Planos"
2. Clique "Criar Novo Plano" várias vezes
3. Veja vários planos listados
4. Teste deletar alguns

### Acompanhar Progresso
1. Registre progresso com pesos diferentes
2. Veja como os valores mudam
3. Observar a sequência de datas

### Testar Pontos
1. Comece com X pontos
2. Registre um treino
3. Ganhe 100 pontos
4. Veja o novo total no dashboard

### Testar Validações
1. Tente registrar treino sem duração
2. Tente registrar peso sem valor
3. Verifique as mensagens de erro

---

## Dados do Banco de Dados

### Arquivo do Banco
```
backend/evolua.db
```

### Tabelas Criadas
- `users` - Usuários da aplicação
- `exercises` - Catálogo de exercícios
- `plans` - Planos de treino
- `plan_weeks` - Semanas do plano
- `training_sessions` - Sessões de treino
- `session_exercises` - Exercícios por sessão
- `workouts` - Treinos registrados
- `exercise_logs` - Logs de execução
- `progress` - Registros de progresso
- `medals` - Medalhas conquistadas

---

## Reset de Dados

Para limpar tudo e começar novamente:

```bash
cd backend
rm evolua.db  # Remove o arquivo do banco
python mock_data.py  # Popula novamente com dados novos
```

---

## Notas Importantes

1. **Sem autenticação real:** O sistema não valida senhas atualmente
2. **Dados fictícios:** Emails, fotos e URLs são exemplos
3. **Datas automáticas:** Os treinos são criados com datas nos últimos 30 dias
4. **Pontos calculados:** Baseado no número de treinos (100 por treino)
5. **Medalhas automáticas:** Atribuídas baseado no número de treinos

---

## Solução de Problemas

### "Banco de dados vazio"
```bash
cd backend
python mock_data.py
```

### "Erro de arquivo não encontrado"
Certifique-se de estar na pasta `backend` ao executar o script

### "Dados não aparecem no frontend"
- Verifique se o backend está rodando em `http://localhost:5000`
- Abra o console do navegador (F12) para ver erros
- Verifique a aba Network para requisições

---

Aproveite os testes! 🧪
