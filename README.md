# Evolua - Sistema de Treinamento Personalizado

Evolua é uma aplicação web completa para treinamento físico personalizado, desenvolvida em Python com Flask no backend e JavaScript vanilla no frontend.

## Visão Geral do Projeto

O Evolua resolve o problema da alta taxa de desistência em atividades físicas oferecendo:

- **Planos de treino personalizados com IA** - Adaptáveis ao seu objetivo, nível e disponibilidade
- **Guias de execução com vídeos** - Aprenda a forma correta de cada exercício
- **Gamificação e recompensas** - Ganhe pontos e medalhas para manter a motivação
- **Monitoramento de evolução** - Acompanhe seu progresso com gráficos e fotos

## Estrutura do Projeto

```
evolua-app/
├── backend/
│   ├── app.py              # Aplicação Flask principal
│   ├── config.py           # Configurações da aplicação
│   ├── models.py           # Modelos de banco de dados
│   ├── requirements.txt     # Dependências Python
│   └── .env.example         # Exemplo de variáveis de ambiente
├── frontend/
│   ├── index.html          # HTML principal
│   ├── styles.css          # Estilos CSS
│   ├── app.js              # Lógica JavaScript
│   └── api.js              # Cliente API
├── docs/
│   └── API.md              # Documentação da API
└── README.md               # Este arquivo
```

## Requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)
- Navegador web moderno

## Instalação

### 1. Clonar o repositório

```bash
git clone <repository-url>
cd evolua-app
```

### 2. Configurar Backend

```bash
cd backend

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# No Linux/Mac:
source venv/bin/activate
# No Windows:
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Copiar arquivo de exemplo de ambiente
cp .env.example .env
```

### 3. Executar Backend

```bash
python app.py
```

O backend estará disponível em `http://localhost:5000`

### 4. Executar Frontend

```bash
cd frontend

# Usar um servidor HTTP simples (Python 3)
python -m http.server 8000
```

O frontend estará disponível em `http://localhost:8000`

## Uso

1. Abra `http://localhost:8000` no seu navegador
2. Faça login ou registre uma nova conta
3. Complete seu perfil com seus dados
4. Crie um plano de treino personalizado
5. Comece a registrar seus treinos e acompanhe seu progresso

## API Endpoints

### Users
- `POST /api/users` - Criar novo usuário
- `GET /api/users/<user_id>` - Obter dados do usuário
- `PUT /api/users/<user_id>` - Atualizar dados do usuário

### Exercises
- `GET /api/exercises` - Listar exercícios
- `POST /api/exercises` - Criar novo exercício

### Plans
- `POST /api/plans` - Criar novo plano de treino
- `GET /api/plans/<plan_id>` - Obter detalhes do plano

### Workouts
- `POST /api/workouts` - Registrar treino concluído
- `GET /api/workouts/<user_id>` - Obter histórico de treinos

### Progress
- `POST /api/progress` - Registrar progresso
- `GET /api/progress/<user_id>` - Obter histórico de progresso

### Medals
- `GET /api/medals/<user_id>` - Obter medalhas do usuário
- `POST /api/medals` - Atribuir medalha

## Banco de Dados

O projeto usa SQLAlchemy com SQLite por padrão. Os modelos incluem:

- **User** - Dados do usuário
- **Plan** - Plano de treino
- **PlanWeek** - Semana do plano
- **TrainingSession** - Sessão de treino
- **SessionExercise** - Exercício em uma sessão
- **Exercise** - Catálogo de exercícios
- **Workout** - Treino registrado
- **ExerciseLog** - Log individual de exercício
- **Progress** - Registro de progresso
- **Medal** - Medalhas conquistadas

## Funcionalidades

### Perfil do Usuário
- Nome, email, idade
- Objetivo (ganho de massa, perda de peso, tonificação)
- Nível (iniciante, intermediário, avançado)
- Dias de treino por semana
- Local de treino (academia, casa, parque)

### Planos de Treino
- Criação automática baseada no perfil
- Estrutura semanal
- Múltiplas sessões de treino
- Exercícios com séries e repetições

### Registros de Treino
- Data e duração
- Peso total levantado
- Calorias queimadas
- Notas e feedback

### Acompanhamento de Progresso
- Peso corporal
- Fotos antes/depois
- Medidas corporais
- Histórico completo

### Gamificação
- Sistema de pontos
- Medalhas por conquistas
- Streak de treinos

## Desenvolvimento

### Estrutura do Backend

O backend é uma aplicação Flask com:
- Blueprint de rotas por funcionalidade
- Modelos SQLAlchemy para persistência
- CORS habilitado para aceitar requisições do frontend
- Tratamento de erros e validação

### Estrutura do Frontend

O frontend é uma SPA (Single Page Application) com:
- Navegação entre páginas sem reload
- Requisições AJAX para API
- Armazenamento local (localStorage)
- Design responsivo com CSS Grid/Flexbox

## Próximos Passos

- [ ] Autenticação com JWT
- [ ] Integração com IA para geração de planos
- [ ] Vídeos de execução de exercícios
- [ ] Sistema de comunidade e compartilhamento
- [ ] Notificações push
- [ ] Aplicativo mobile com React Native
- [ ] Dashboard administrativo
- [ ] Integração com sensores/wearables

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT.

## Autores

- Davi de Tássio de Rodrigues Silva
- Felipe Correia Ribeiro
- Mayara Angelica da Silva
- Rodrigo dos Santos Silva
- Vitor da Silva Moreira
- João Pedro Lopes dos Santos

## Contato

Para mais informações, visite [seu-site.com](http://seu-site.com) ou envie um email para contato@evolua.com
