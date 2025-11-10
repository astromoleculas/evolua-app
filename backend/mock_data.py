"""
Script para popular o banco de dados com dados de teste
"""

from app import app, db
from models import (
    User, Exercise, Plan, PlanWeek, TrainingSession, SessionExercise,
    Workout, ExerciseLog, Progress, Medal
)
from datetime import datetime, timedelta
import json

def clear_database():
    """Limpa todas as tabelas do banco de dados"""
    db.drop_all()
    db.create_all()
    print("✓ Banco de dados limpo")

def seed_exercises():
    """Adiciona exercícios de exemplo ao banco de dados"""

    exercises = [
        # Peito
        Exercise(
            name="Supino Reto com Halteres",
            muscle_group="Peito",
            difficulty="Intermediario",
            description="Exercício fundamental para desenvolvimento do peito",
            instructions="1. Deite-se no banco com pés apoiados no chão\n2. Mantenha os halteres ao nível do peito\n3. Pressione os halteres para cima\n4. Abaixe controladamente",
            safety_tips="Mantenha os cotovelos estáveis. Não jogue os halteres. Use peso apropriado.",
            video_url="https://example.com/supino-reto.mp4"
        ),
        Exercise(
            name="Flexão no Banco",
            muscle_group="Peito",
            difficulty="Iniciante",
            description="Variante mais fácil da flexão tradicional",
            instructions="1. Coloque as mãos no banco\n2. Corpo esticado\n3. Desça dobrando os cotovelos\n4. Suba estendendo os braços",
            safety_tips="Mantenha o corpo reto. Controle o movimento.",
            video_url="https://example.com/flexao-banco.mp4"
        ),
        Exercise(
            name="Supino Inclinado",
            muscle_group="Peito",
            difficulty="Intermediario",
            description="Exercício para desenvolvimento da parte superior do peito",
            instructions="1. Deite-se no banco inclinado a 45 graus\n2. Halteres ao nível do peito\n3. Pressione para cima em ângulo",
            safety_tips="Cuidado com a estabilidade no banco inclinado",
            video_url="https://example.com/supino-inclinado.mp4"
        ),

        # Costas
        Exercise(
            name="Puxada Frontal",
            muscle_group="Costas",
            difficulty="Intermediario",
            description="Exercício para desenvolvimento das costas",
            instructions="1. Sente-se na máquina\n2. Pegue a barra com as mãos afastadas\n3. Puxe a barra em direção ao peito\n4. Suba controladamente",
            safety_tips="Evite usar movimento de corpo. Mantenha as costas retas.",
            video_url="https://example.com/puxada-frontal.mp4"
        ),
        Exercise(
            name="Remada Inclinada",
            muscle_group="Costas",
            difficulty="Intermediario",
            description="Excelente para estruturar as costas",
            instructions="1. Incline o tronco em 45 graus\n2. Mantenha os joelhos ligeiramente flexionados\n3. Puxe os halteres em direção ao abdômen\n4. Abaixe controladamente",
            safety_tips="Cuidado com a coluna. Não balance o corpo.",
            video_url="https://example.com/remada-inclinada.mp4"
        ),
        Exercise(
            name="Barra Fixa",
            muscle_group="Costas",
            difficulty="Avancado",
            description="Exercício avançado para costas",
            instructions="1. Agarre a barra com mãos afastadas\n2. Suba puxando o corpo\n3. Desça controladamente",
            safety_tips="Exige força considerável",
            video_url="https://example.com/barra-fixa.mp4"
        ),

        # Pernas
        Exercise(
            name="Supino para Pernas",
            muscle_group="Perna",
            difficulty="Iniciante",
            description="Seguro e eficaz para treinar pernas",
            instructions="1. Sente-se na máquina\n2. Coloque os pés na plataforma\n3. Estenda as pernas\n4. Flexione voltando",
            safety_tips="Não estique completamente o joelho. Mantenha o movimento controlado.",
            video_url="https://example.com/supino-pernas.mp4"
        ),
        Exercise(
            name="Agachamento com Peso",
            muscle_group="Perna",
            difficulty="Avancado",
            description="Exercício fundamental para força nas pernas",
            instructions="1. De pé com os pés afastados na largura dos ombros\n2. Barra nos ombros\n3. Abaixe como se fosse sentar\n4. Suba estendendo as pernas",
            safety_tips="Mantenha as costas retas. Joelhos não passem a ponta do pé.",
            video_url="https://example.com/agachamento.mp4"
        ),
        Exercise(
            name="Legpress",
            muscle_group="Perna",
            difficulty="Intermediario",
            description="Máquina excelente para pernas",
            instructions="1. Sente-se na máquina\n2. Coloque os pés na plataforma\n3. Estenda as pernas empurrando\n4. Flexione voltando",
            safety_tips="Não estique completamente o joelho. Respirar é importante.",
            video_url="https://example.com/legpress.mp4"
        ),
        Exercise(
            name="Rosca Direta de Pernas",
            muscle_group="Perna",
            difficulty="Iniciante",
            description="Isolamento para quadríceps",
            instructions="1. Sente-se na máquina\n2. Coloque os pés sob a alavanca\n3. Estenda as pernas\n4. Abaixe controladamente",
            safety_tips="Movimento controlado e suave",
            video_url="https://example.com/rosca-pernas.mp4"
        ),

        # Braços
        Exercise(
            name="Rosca Direta",
            muscle_group="Braço",
            difficulty="Iniciante",
            description="Exercício fundamental para bíceps",
            instructions="1. De pé com halteres nas mãos\n2. Braços estendidos\n3. Flexione os cotovelos levantando os halteres\n4. Abaixe controladamente",
            safety_tips="Não oscile o corpo. Mantenha os cotovelos próximos ao corpo.",
            video_url="https://example.com/rosca-direta.mp4"
        ),
        Exercise(
            name="Rosca Inversa",
            muscle_group="Braço",
            difficulty="Intermediario",
            description="Exercício para bíceps e antebraço",
            instructions="1. De pé com halteres nas mãos com as palmas viradas para baixo\n2. Braços estendidos\n3. Flexione os cotovelos\n4. Abaixe controladamente",
            safety_tips="Mantenha os cotovelos imóveis. Controle o movimento.",
            video_url="https://example.com/rosca-inversa.mp4"
        ),
        Exercise(
            name="Extensão de Tríceps",
            muscle_group="Braço",
            difficulty="Iniciante",
            description="Isolamento para tríceps",
            instructions="1. De pé com o haltere atrás da cabeça\n2. Estenda os braços para cima\n3. Abaixe trazendo o haltere atrás da cabeça",
            safety_tips="Mantenha os cotovelos apontados para frente. Movimento controlado.",
            video_url="https://example.com/extensao-triceps.mp4"
        ),
        Exercise(
            name="Rosca Concentrada",
            muscle_group="Braço",
            difficulty="Intermediario",
            description="Isolamento intenso para bíceps",
            instructions="1. Sente-se com os cotovelos apoiados nas coxas\n2. Levante o haltere\n3. Abaixe controladamente",
            safety_tips="Movimento isolado e controlado",
            video_url="https://example.com/rosca-concentrada.mp4"
        ),

        # Ombros
        Exercise(
            name="Desenvolvimento com Halteres",
            muscle_group="Ombro",
            difficulty="Intermediario",
            description="Exercício essencial para desenvolvimento de ombros",
            instructions="1. De pé ou sentado com halteres ao nível dos ombros\n2. Estenda os braços para cima\n3. Abaixe voltando à posição inicial",
            safety_tips="Não arquear a coluna. Movimento controlado.",
            video_url="https://example.com/desenvolvimento.mp4"
        ),
        Exercise(
            name="Elevação Lateral",
            muscle_group="Ombro",
            difficulty="Iniciante",
            description="Isolamento para ombro lateral",
            instructions="1. De pé com halteres nas laterais\n2. Levante os halteres até a altura dos ombros\n3. Abaixe controladamente",
            safety_tips="Cotovelos ligeiramente flexionados. Evite balanço.",
            video_url="https://example.com/elevacao-lateral.mp4"
        ),
        Exercise(
            name="Encolhimento de Ombros",
            muscle_group="Ombro",
            difficulty="Iniciante",
            description="Exercício para trapézio",
            instructions="1. De pé com halteres nas laterais\n2. Levante os ombros em direção às orelhas\n3. Abaixe controladamente",
            safety_tips="Movimento pequeno e controlado",
            video_url="https://example.com/encolhimento.mp4"
        ),
    ]

    for exercise in exercises:
        db.session.add(exercise)

    db.session.commit()
    print(f"✓ {len(exercises)} exercícios adicionados")


def seed_users():
    """Adiciona usuários de teste"""

    users = [
        User(
            name="Carlos Mendes",
            email="carlos@example.com",
            password_hash="hashed_password_123",
            age=21,
            objective="ganho_massa",
            level="iniciante",
            days_per_week=3,
            training_location="academia",
            points=450
        ),
        User(
            name="Juliana Lima",
            email="juliana@example.com",
            password_hash="hashed_password_456",
            age=34,
            objective="perda_peso",
            level="intermediario",
            days_per_week=4,
            training_location="casa",
            points=750
        ),
        User(
            name="João Silva",
            email="joao@example.com",
            password_hash="hashed_password_789",
            age=28,
            objective="tonificacao",
            level="intermediario",
            days_per_week=5,
            training_location="academia",
            points=600
        ),
    ]

    for user in users:
        db.session.add(user)

    db.session.commit()
    print(f"✓ {len(users)} usuários adicionados")
    return users


def seed_plans_and_sessions(users):
    """Adiciona planos de treino para os usuários"""

    plans = []

    for user in users:
        plan = Plan(
            user_id=user.id,
            name=f"Plano {user.objective} - {user.level}",
            description=f"Plano personalizado de {user.days_per_week} dias por semana",
            duration_weeks=12,
            created_at=datetime.utcnow() - timedelta(days=30)
        )
        db.session.add(plan)
        db.session.flush()

        # Criar 4 semanas
        for week_num in range(1, 5):
            plan_week = PlanWeek(
                plan_id=plan.id,
                week_number=week_num
            )
            db.session.add(plan_week)
            db.session.flush()

            # Criar sessões de treino baseado nos dias da semana do usuário
            days = list(range(user.days_per_week))
            session_names = ['A', 'B', 'C', 'D', 'E']
            focus_groups = ['Peito e Tríceps', 'Costas e Bíceps', 'Perna', 'Ombro', 'Cardio']

            for idx, day in enumerate(days):
                session = TrainingSession(
                    plan_week_id=plan_week.id,
                    session_name=f"Treino {session_names[idx]}",
                    day_of_week=day,
                    focus_group=focus_groups[idx % len(focus_groups)]
                )
                db.session.add(session)

        plans.append(plan)

    db.session.commit()
    print(f"✓ {len(plans)} planos e sessões adicionados")
    return plans


def seed_workouts(users):
    """Adiciona histórico de treinos"""

    workouts = []
    now = datetime.utcnow()

    for user in users:
        # Criar treinos dos últimos 30 dias
        for i in range(1, 15):  # 14 treinos por usuário
            workout = Workout(
                user_id=user.id,
                date=now - timedelta(days=i),
                duration_minutes=45 + (i % 30),  # Entre 45 e 75 minutos
                total_weight=200 + (i * 20),
                calories_burned=300 + (i * 10),
                completed=True,
                notes=f"Treino #{i} - Excelente desempenho!" if i % 2 == 0 else f"Treino #{i} - Bom desempenho"
            )
            db.session.add(workout)
            workouts.append(workout)

    db.session.commit()
    print(f"✓ {len(workouts)} treinos adicionados")
    return workouts


def seed_progress(users):
    """Adiciona registros de progresso"""

    progress_records = []
    now = datetime.utcnow()

    for user in users:
        # Criar 4 registros de progresso (a cada semana)
        base_weight = 80 if user.objective == "perda_peso" else 70

        for i in range(4):
            progress = Progress(
                user_id=user.id,
                date=now - timedelta(days=28 - (i * 7)),
                weight=base_weight - (i * 1.5) if user.objective == "perda_peso" else base_weight + (i * 0.5),
                body_measurements={
                    "chest": 100 + (i * 2),
                    "waist": 85 - (i * 1),
                    "arm": 30 + (i * 0.5),
                    "thigh": 55 + (i * 1),
                },
                photo_url=f"https://example.com/user-{user.id}-week-{i+1}.jpg",
                notes=f"Semana {i+1} - Progresso visível" if i > 0 else "Foto inicial"
            )
            db.session.add(progress)
            progress_records.append(progress)

    db.session.commit()
    print(f"✓ {len(progress_records)} registros de progresso adicionados")
    return progress_records


def seed_medals(users):
    """Adiciona medalhas conquistadas"""

    medals_list = []
    medal_types = [
        {"name": "Primeira Semana", "icon": "bronze", "description": "Completou a primeira semana"},
        {"name": "Mês Completo", "icon": "silver", "description": "Completou um mês inteiro"},
        {"name": "Persistência de Aço", "icon": "gold", "description": "30 treinos completados"},
        {"name": "Rei do Treino", "icon": "platinum", "description": "50 treinos completados"},
    ]

    for user in users:
        # Dar medalhas baseado no número de treinos do usuário
        num_medals = min(4, (user.points // 200) + 1)

        for i in range(num_medals):
            medal_type = medal_types[i]
            medal = Medal(
                user_id=user.id,
                name=medal_type["name"],
                description=medal_type["description"],
                icon=medal_type["icon"],
                earned_at=datetime.utcnow() - timedelta(days=30 - (i * 7))
            )
            db.session.add(medal)
            medals_list.append(medal)

    db.session.commit()
    print(f"✓ {len(medals_list)} medalhas adicionadas")
    return medals_list


def populate_database():
    """Função principal para popular o banco de dados"""

    with app.app_context():
        print("\n" + "="*50)
        print("Populando banco de dados com dados de teste")
        print("="*50 + "\n")

        # Limpar banco anterior
        clear_database()

        # Popular dados
        seed_exercises()
        users = seed_users()
        plans = seed_plans_and_sessions(users)
        workouts = seed_workouts(users)
        progress = seed_progress(users)
        medals = seed_medals(users)

        print("\n" + "="*50)
        print("✓ Banco de dados populado com sucesso!")
        print("="*50)
        print("\nDados de teste criados:")
        print(f"  - {len(users)} usuários")
        print(f"  - {len(plans)} planos de treino")
        print(f"  - {len(workouts)} treinos registrados")
        print(f"  - {len(progress)} registros de progresso")
        print(f"  - {len(medals)} medalhas")
        print("\nUsuários de teste para login:")
        for user in users:
            print(f"  - Email: {user.email} | Objetivo: {user.objective}")
        print("\n")


if __name__ == '__main__':
    populate_database()
