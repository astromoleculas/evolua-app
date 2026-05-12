"""
EVOLUA - Backend API completo com Flask
Inclui: Autenticação JWT, geração de planos, execução de treinos, gamificação, progresso
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from config import DevelopmentConfig
from models import db, User, Plan, PlanWeek, TrainingSession, SessionExercise, Exercise, Workout, ExerciseLog, Progress, Medal
from datetime import datetime, timedelta, date
import random
from functools import wraps

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.config['JWT_SECRET_KEY'] = app.config.get('SECRET_KEY', 'evolua-secret-2024')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)
CORS(app)

# Create database tables
with app.app_context():
    db.create_all()

# ==================== EXERCÍCIOS PADRÃO ====================

DEFAULT_EXERCISES = [
    {
        'name': 'Supino com Halteres',
        'muscle_group': 'Peito',
        'difficulty': 'Intermediário',
        'instructions': 'Deitado em banco plano, abaixe o haltere até o peito e suba',
        'safety_tips': 'Mantenha o controle do movimento. Não balance o corpo.',
        'video_url': 'https://example.com/videos/supino-halteres.mp4'
    },
    {
        'name': 'Rosca Direta',
        'muscle_group': 'Braço - Bíceps',
        'difficulty': 'Iniciante',
        'instructions': 'De pé, com os halteres ao lado do corpo, flexione os cotovelos',
        'safety_tips': 'Cotovelos fixos ao corpo. Movimento controlado.',
        'video_url': 'https://example.com/videos/rosca-direta.mp4'
    },
    {
        'name': 'Leg Press',
        'muscle_group': 'Perna',
        'difficulty': 'Iniciante',
        'instructions': 'Sentado, empurre a plataforma com as pernas até extensão completa',
        'safety_tips': 'Não tranque os joelhos. Mantenha a postura ereta.',
        'video_url': 'https://example.com/videos/leg-press.mp4'
    },
    {
        'name': 'Puxada Frontal',
        'muscle_group': 'Costas',
        'difficulty': 'Intermediário',
        'instructions': 'Sentado, puxe a barra em sua direção até o peito',
        'safety_tips': 'Não arque excessivamente. Controle a descida.',
        'video_url': 'https://example.com/videos/puxada-frontal.mp4'
    },
    {
        'name': 'Agachamento Livre',
        'muscle_group': 'Perna',
        'difficulty': 'Intermediário',
        'instructions': 'De pé, desça mantendo as costas retas até formar ângulo de 90°',
        'safety_tips': 'Joelhos alineados com os pés. Evite deslocar o joelho para frente.',
        'video_url': 'https://example.com/videos/agachamento.mp4'
    },
    {
        'name': 'Abdominal Crunches',
        'muscle_group': 'Abdômen',
        'difficulty': 'Iniciante',
        'instructions': 'Deitado, levante o tronco contraindo o abdômen',
        'safety_tips': 'Não force o pescoço. Movimento controlado.',
        'video_url': 'https://example.com/videos/crunches.mp4'
    },
    {
        'name': 'Barra Fixa',
        'muscle_group': 'Costas',
        'difficulty': 'Avançado',
        'instructions': 'Suspenso, puxe seu corpo até que o queixo ultrapasse a barra',
        'safety_tips': 'Controle o movimento. Não balance.',
        'video_url': 'https://example.com/videos/barra-fixa.mp4'
    },
    {
        'name': 'Desenvolvimento de Ombro',
        'muscle_group': 'Ombro',
        'difficulty': 'Intermediário',
        'instructions': 'Sentado, empurre o haltere acima da cabeça',
        'safety_tips': 'Mantenha o core engajado. Não arqueia a coluna.',
        'video_url': 'https://example.com/videos/desenvolvimento-ombro.mp4'
    }
]

WORKOUT_PLANS = {
    'iniciante': {
        'hipertrofia': {
            'treino_a': {
                'nome': 'Peito e Tríceps',
                'exercicios': ['Supino com Halteres', 'Rosca Direta', 'Abdominal Crunches']
            },
            'treino_b': {
                'nome': 'Costas e Bíceps',
                'exercicios': ['Puxada Frontal', 'Rosca Direta', 'Abdominal Crunches']
            },
            'treino_c': {
                'nome': 'Perna e Ombro',
                'exercicios': ['Leg Press', 'Desenvolvimento de Ombro', 'Abdominal Crunches']
            }
        },
        'perda_peso': {
            'treino_a': {
                'nome': 'Full Body A',
                'exercicios': ['Agachamento Livre', 'Supino com Halteres', 'Puxada Frontal']
            },
            'treino_b': {
                'nome': 'Full Body B',
                'exercicios': ['Leg Press', 'Desenvolvimento de Ombro', 'Rosca Direta']
            },
            'treino_c': {
                'nome': 'Full Body C',
                'exercicios': ['Abdominal Crunches', 'Puxada Frontal', 'Agachamento Livre']
            }
        }
    }
}

# ==================== HELPER FUNCTIONS ====================

def initialize_exercises():
    """Carrega exercícios padrão no banco se não existem"""
    with app.app_context():
        for exc_data in DEFAULT_EXERCISES:
            if not Exercise.query.filter_by(name=exc_data['name']).first():
                exc = Exercise(**exc_data)
                db.session.add(exc)
        db.session.commit()

def generate_workout_plan(user_id, objective='hipertrofia'):
    """Gera um plano de treino personalizado"""
    user = User.query.get(user_id)
    if not user:
        return None

    plan_data = WORKOUT_PLANS.get('iniciante', {}).get(objective, {})
    
    plan = Plan(
        user_id=user_id,
        name=f"Plano {user.objective.title()} - {datetime.now().strftime('%B %Y')}",
        description=f"Plano personalizado para {objective.replace('_', ' ')}",
        duration_weeks=12
    )
    db.session.add(plan)
    db.session.flush()

    # Create first week
    week = PlanWeek(plan_id=plan.id, week_number=1)
    db.session.add(week)
    db.session.flush()

    # Create training sessions
    days = {
        'treino_a': {'day': 1, 'name': 'Treino A'},
        'treino_b': {'day': 3, 'name': 'Treino B'},
        'treino_c': {'day': 5, 'name': 'Treino C'}
    }

    for session_key, session_info in days.items():
        if session_key in plan_data:
            session = TrainingSession(
                plan_week_id=week.id,
                session_name=session_info['name'],
                day_of_week=session_info['day'],
                focus_group=plan_data[session_key].get('nome', 'General')
            )
            db.session.add(session)
            db.session.flush()

            # Add exercises
            for idx, exc_name in enumerate(plan_data[session_key].get('exercicios', [])):
                exercise = Exercise.query.filter_by(name=exc_name).first()
                if exercise:
                    session_exc = SessionExercise(
                        training_session_id=session.id,
                        exercise_id=exercise.id,
                        sets=3,
                        reps='8-12',
                        rest_seconds=60,
                        order=idx + 1
                    )
                    db.session.add(session_exc)

    db.session.commit()
    return plan

def award_medal(user_id, medal_name, description, icon):
    """Atribui uma medalha ao usuário"""
    medal = Medal(
        user_id=user_id,
        name=medal_name,
        description=description,
        icon=icon
    )
    db.session.add(medal)
    db.session.commit()
    return medal

def check_and_award_medals(user_id):
    """Verifica e atribui medalhas baseado em conquistas"""
    user = User.query.get(user_id)
    workouts_count = Workout.query.filter_by(user_id=user_id, completed=True).count()
    
    medal_awarded = None
    
    if workouts_count == 1 and not Medal.query.filter_by(user_id=user_id, name='Primeira Semana').first():
        medal_awarded = award_medal(user_id, 'Primeira Semana', 'Completou seu primeiro treino!', 'bronze')
    elif workouts_count == 10 and not Medal.query.filter_by(user_id=user_id, name='Dedicado').first():
        medal_awarded = award_medal(user_id, 'Dedicado', 'Completou 10 treinos!', 'silver')
    elif workouts_count == 50 and not Medal.query.filter_by(user_id=user_id, name='Campeão').first():
        medal_awarded = award_medal(user_id, 'Campeão', 'Completou 50 treinos!', 'gold')
    
    return medal_awarded

# ==================== AUTENTICAÇÃO ====================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Registrar novo usuário"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password') or not data.get('name'):
        return jsonify({'error': 'Email, password e name são obrigatórios'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email já cadastrado'}), 409
    
    user = User(
        name=data['name'],
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        age=data.get('age'),
        objective=data.get('objective', 'hipertrofia'),
        level=data.get('level', 'iniciante'),
        days_per_week=data.get('days_per_week', 3),
        training_location=data.get('training_location', 'academia')
    )
    
    db.session.add(user)
    db.session.commit()
    
    access_token = create_access_token(identity=str(user.id))
    
    return jsonify({
        'message': 'Usuário criado com sucesso',
        'user_id': user.id,
        'access_token': access_token
    }), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login do usuário"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email e password são obrigatórios'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Email ou senha incorretos'}), 401
    
    access_token = create_access_token(identity=str(user.id))
    
    return jsonify({
        'access_token': access_token,
        'user_id': user.id,
        'name': user.name
    }), 200

# ==================== USUÁRIO ====================

@app.route('/api/users/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Obter perfil do usuário autenticado"""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'age': user.age,
        'objective': user.objective,
        'level': user.level,
        'days_per_week': user.days_per_week,
        'training_location': user.training_location,
        'points': user.points,
        'created_at': user.created_at.isoformat(),
        'updated_at': user.updated_at.isoformat()
    }), 200

@app.route('/api/users/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Atualizar perfil do usuário"""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    data = request.get_json()
    
    if 'name' in data:
        user.name = data['name']
    if 'age' in data:
        user.age = data['age']
    if 'objective' in data:
        user.objective = data['objective']
    if 'level' in data:
        user.level = data['level']
    if 'days_per_week' in data:
        user.days_per_week = data['days_per_week']
    if 'training_location' in data:
        user.training_location = data['training_location']
    
    user.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({'message': 'Perfil atualizado com sucesso'}), 200

# ==================== PLANOS DE TREINO ====================

@app.route('/api/plans', methods=['GET'])
@jwt_required()
def get_plans():
    """Obter planos de treino do usuário"""
    user_id = int(get_jwt_identity())
    plans = Plan.query.filter_by(user_id=user_id).all()
    
    return jsonify([{
        'id': plan.id,
        'name': plan.name,
        'description': plan.description,
        'duration_weeks': plan.duration_weeks,
        'created_at': plan.created_at.isoformat(),
        'updated_at': plan.updated_at.isoformat()
    } for plan in plans]), 200

@app.route('/api/plans', methods=['POST'])
@jwt_required()
def create_plan():
    """Criar novo plano de treino (gera automaticamente com IA básica)"""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    plan = generate_workout_plan(user_id, objective=user.objective or 'hipertrofia')
    
    if not plan:
        return jsonify({'error': 'Erro ao gerar plano'}), 500
    
    return jsonify({
        'message': 'Plano de treino criado com sucesso',
        'plan_id': plan.id,
        'name': plan.name
    }), 201

@app.route('/api/plans/<int:plan_id>', methods=['GET'])
@jwt_required()
def get_plan_details(plan_id):
    """Obter detalhes do plano com exercícios"""
    user_id = int(get_jwt_identity())
    plan = Plan.query.filter_by(id=plan_id, user_id=user_id).first()
    
    if not plan:
        return jsonify({'error': 'Plano não encontrado'}), 404
    
    weeks = []
    for week in plan.weeks:
        sessions = []
        for session in week.sessions:
            exercises = []
            for session_exc in session.exercises:
                exercises.append({
                    'id': session_exc.exercise_id,
                    'name': session_exc.exercise.name,
                    'sets': session_exc.sets,
                    'reps': session_exc.reps,
                    'rest_seconds': session_exc.rest_seconds,
                    'video_url': session_exc.exercise.video_url
                })
            
            sessions.append({
                'id': session.id,
                'name': session.session_name,
                'day': session.day_of_week,
                'focus': session.focus_group,
                'exercises': exercises
            })
        
        weeks.append({
            'number': week.week_number,
            'sessions': sessions
        })
    
    return jsonify({
        'id': plan.id,
        'name': plan.name,
        'description': plan.description,
        'weeks': weeks
    }), 200

# ==================== EXECUÇÃO DE TREINOS ====================

@app.route('/api/workouts', methods=['POST'])
@jwt_required()
def create_workout():
    """Criar novo registro de treino"""
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    workout = Workout(
        user_id=user_id,
        training_session_id=data.get('training_session_id'),
        duration_minutes=data.get('duration_minutes', 0),
        completed=False
    )
    
    db.session.add(workout)
    db.session.commit()
    
    return jsonify({
        'workout_id': workout.id,
        'date': workout.date.isoformat(),
        'completed': workout.completed
    }), 201

@app.route('/api/workouts/<int:workout_id>/exercise', methods=['POST'])
@jwt_required()
def log_exercise(workout_id):
    """Registrar exercício realizado"""
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    workout = Workout.query.filter_by(id=workout_id, user_id=user_id).first()
    if not workout:
        return jsonify({'error': 'Treino não encontrado'}), 404
    
    exercise_log = ExerciseLog(
        workout_id=workout_id,
        exercise_id=data['exercise_id'],
        sets_completed=data.get('sets_completed', 0),
        actual_reps=data.get('actual_reps', []),
        weight_per_set=data.get('weight_per_set', []),
        difficulty_feedback=data.get('difficulty_feedback', 'normal'),
        completed=True
    )
    
    db.session.add(exercise_log)
    
    # Award points
    user = User.query.get(user_id)
    user.points += 10  # 10 pontos por exercício completado
    
    db.session.commit()
    
    return jsonify({'message': 'Exercício registrado com sucesso'}), 201

@app.route('/api/workouts/<int:workout_id>/complete', methods=['PUT'])
@jwt_required()
def complete_workout(workout_id):
    """Marcar treino como completo"""
    user_id = int(get_jwt_identity())
    
    workout = Workout.query.filter_by(id=workout_id, user_id=user_id).first()
    if not workout:
        return jsonify({'error': 'Treino não encontrado'}), 404
    
    workout.completed = True
    workout.duration_minutes = request.get_json().get('duration_minutes', 0)
    
    # Calculate total weight lifted
    total_weight = 0
    for log in workout.exercises_log:
        if log.weight_per_set:
            try:
                if isinstance(log.weight_per_set, list):
                    total_weight += sum(float(w) if w else 0 for w in log.weight_per_set)
                else:
                    total_weight += float(log.weight_per_set)
            except (TypeError, ValueError):
                pass
    workout.total_weight = total_weight
    
    # Award bonus points for completion
    user = User.query.get(user_id)
    user.points += 50  # 50 pontos bônus por completar treino
    
    # Checar medalhas
    medal = check_and_award_medals(user_id)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Treino marcado como completo',
        'points_earned': 50,
        'medal_earned': medal.name if medal else None
    }), 200

@app.route('/api/workouts/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_workouts(user_id):
    """Obter histórico de treinos do usuário (apenas finalizados)"""
    current_user = get_jwt_identity()
    
    if int(current_user) != user_id:
        return jsonify({'error': 'Acesso negado'}), 403
    
    # Retornar apenas treinos completos (completed=True)
    workouts = Workout.query.filter_by(user_id=user_id, completed=True).order_by(Workout.date.desc()).all()
    
    return jsonify([{
        'id': w.id,
        'date': w.date.isoformat(),
        'duration_minutes': w.duration_minutes,
        'total_weight': w.total_weight,
        'completed': w.completed,
        'exercises_count': len(w.exercises_log)
    } for w in workouts]), 200

# ==================== GAMIFICAÇÃO ====================

@app.route('/api/medals/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_medals(user_id):
    """Obter medalhas conquistadas"""
    current_user = get_jwt_identity()
    
    if int(current_user) != user_id:
        return jsonify({'error': 'Acesso negado'}), 403
    
    medals = Medal.query.filter_by(user_id=user_id).all()
    
    return jsonify([{
        'id': m.id,
        'name': m.name,
        'description': m.description,
        'icon': m.icon,
        'earned_at': m.earned_at.isoformat()
    } for m in medals]), 200

@app.route('/api/stats/<int:user_id>', methods=['GET'])
@jwt_required()
def get_stats(user_id):
    """Obter estatísticas do usuário"""
    current_user = get_jwt_identity()
    
    if int(current_user) != user_id:
        return jsonify({'error': 'Acesso negado'}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    workouts_count = Workout.query.filter_by(user_id=user_id, completed=True).count()
    medals_count = Medal.query.filter_by(user_id=user_id).count()
    total_weight = db.session.query(db.func.sum(Workout.total_weight)).filter_by(
        user_id=user_id, completed=True
    ).scalar() or 0
    
    # Calculate streak
    streak = 0
    today = datetime.utcnow().date()
    for i in range(100):
        date = today - timedelta(days=i)
        if Workout.query.filter_by(user_id=user_id, completed=True).filter(
            db.func.date(Workout.date) == date
        ).first():
            streak += 1
        else:
            break
    
    return jsonify({
        'points': user.points,
        'workouts_completed': workouts_count,
        'medals': medals_count,
        'total_weight_lifted': total_weight,
        'current_streak': streak
    }), 200

# ==================== PROGRESSO ====================

@app.route('/api/progress', methods=['POST'])
@jwt_required()
def log_progress():
    """Registrar progresso (peso, medidas, foto) - máximo um por dia"""
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    # Obter data de hoje (apenas ano, mês, dia)
    today = date.today()
    
    # Verificar se já existe registro de progresso para hoje
    existing_progress = Progress.query.filter(
        Progress.user_id == user_id,
        db.func.date(Progress.date) == today
    ).first()
    
    if existing_progress:
        # Atualizar registro existente
        existing_progress.weight = data.get('weight')
        existing_progress.body_measurements = data.get('body_measurements', {})
        existing_progress.photo_url = data.get('photo_url')
        existing_progress.notes = data.get('notes')
        existing_progress.date = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Progresso atualizado com sucesso (já havia registro de hoje)',
            'progress_id': existing_progress.id,
            'updated': True
        }), 200
    
    # Criar novo registro se não existir para hoje
    progress = Progress(
        user_id=user_id,
        weight=data.get('weight'),
        body_measurements=data.get('body_measurements', {}),
        photo_url=data.get('photo_url'),
        notes=data.get('notes')
    )
    
    db.session.add(progress)
    db.session.commit()
    
    return jsonify({
        'message': 'Progresso registrado com sucesso',
        'progress_id': progress.id,
        'updated': False
    }), 201

@app.route('/api/progress/<int:user_id>', methods=['GET'])
@jwt_required()
def get_progress_history(user_id):
    """Obter histórico de progresso"""
    current_user = get_jwt_identity()
    
    if int(current_user) != user_id:
        return jsonify({'error': 'Acesso negado'}), 403
    
    progress_records = Progress.query.filter_by(user_id=user_id).order_by(Progress.date.desc()).all()
    
    return jsonify([{
        'id': p.id,
        'date': p.date.isoformat(),
        'weight': p.weight,
        'body_measurements': p.body_measurements,
        'photo_url': p.photo_url,
        'notes': p.notes
    } for p in progress_records]), 200

@app.route('/api/progress/<int:progress_id>', methods=['PUT'])
@jwt_required()
def update_progress(progress_id):
    """Atualizar registro de progresso"""
    user_id = int(get_jwt_identity())
    progress = Progress.query.get(progress_id)
    
    if not progress or progress.user_id != user_id:
        return jsonify({'error': 'Registro não encontrado ou acesso negado'}), 403
    
    data = request.get_json()
    
    if 'weight' in data:
        progress.weight = data['weight']
    if 'notes' in data:
        progress.notes = data['notes']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Progresso atualizado com sucesso',
        'id': progress.id,
        'date': progress.date.isoformat(),
        'weight': progress.weight,
        'notes': progress.notes
    }), 200

# ==================== EXERCÍCIOS ====================

@app.route('/api/exercises', methods=['GET'])
def get_exercises():
    """Listar todos os exercícios disponíveis"""
    exercises = Exercise.query.all()
    
    return jsonify([{
        'id': e.id,
        'name': e.name,
        'muscle_group': e.muscle_group,
        'difficulty': e.difficulty,
        'instructions': e.instructions,
        'safety_tips': e.safety_tips,
        'video_url': e.video_url
    } for e in exercises]), 200

# ==================== SAÚDE ====================

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({'status': 'OK', 'timestamp': datetime.utcnow().isoformat()}), 200

# ==================== ERRO HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint não encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Erro interno do servidor'}), 500

# ==================== INITIALIZATION ====================

if __name__ == '__main__':
    with app.app_context():
        # Initialize exercises
        initialize_exercises()
        print("✓ Exercícios padrão carregados")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
