from flask import Flask, jsonify, request
from flask_cors import CORS
from config import DevelopmentConfig
from models import db, User, Plan, Exercise, TrainingSession, Workout, Progress, Medal
from datetime import datetime, timedelta
import json

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Initialize database
db.init_app(app)
CORS(app)

# Create database tables
with app.app_context():
    db.create_all()

# ==================== USER ROUTES ====================

@app.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user"""
    data = request.get_json()

    if not data or not data.get('email') or not data.get('name'):
        return jsonify({'error': 'Missing required fields'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 409

    user = User(
        name=data['name'],
        email=data['email'],
        password_hash=data.get('password', 'hash'),  # In production, use proper hashing
        age=data.get('age'),
        objective=data.get('objective'),
        level=data.get('level'),
        days_per_week=data.get('days_per_week', 3),
        training_location=data.get('training_location')
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'objective': user.objective,
        'level': user.level,
        'points': user.points
    }), 201

@app.route('/api/users/email/<email>', methods=['GET'])
def get_user_by_email(email):
    """Get user by email - for login"""
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

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
        'created_at': user.created_at.isoformat()
    }), 200

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user profile"""
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

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
        'created_at': user.created_at.isoformat()
    }), 200

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user profile"""
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()

    user.name = data.get('name', user.name)
    user.age = data.get('age', user.age)
    user.objective = data.get('objective', user.objective)
    user.level = data.get('level', user.level)
    user.days_per_week = data.get('days_per_week', user.days_per_week)
    user.training_location = data.get('training_location', user.training_location)

    db.session.commit()

    return jsonify({'message': 'User updated successfully'}), 200

# ==================== EXERCISE ROUTES ====================

@app.route('/api/exercises', methods=['GET'])
def get_exercises():
    """Get all exercises"""
    muscle_group = request.args.get('muscle_group')
    difficulty = request.args.get('difficulty')

    query = Exercise.query

    if muscle_group:
        query = query.filter_by(muscle_group=muscle_group)
    if difficulty:
        query = query.filter_by(difficulty=difficulty)

    exercises = query.all()

    return jsonify([{
        'id': ex.id,
        'name': ex.name,
        'muscle_group': ex.muscle_group,
        'difficulty': ex.difficulty,
        'description': ex.description,
        'instructions': ex.instructions,
        'safety_tips': ex.safety_tips,
        'video_url': ex.video_url
    } for ex in exercises]), 200

@app.route('/api/exercises', methods=['POST'])
def create_exercise():
    """Create a new exercise"""
    data = request.get_json()

    if not data or not data.get('name'):
        return jsonify({'error': 'Missing required fields'}), 400

    exercise = Exercise(
        name=data['name'],
        muscle_group=data.get('muscle_group'),
        difficulty=data.get('difficulty', 'Intermediario'),
        description=data.get('description'),
        instructions=data.get('instructions'),
        safety_tips=data.get('safety_tips'),
        video_url=data.get('video_url')
    )

    db.session.add(exercise)
    db.session.commit()

    return jsonify({
        'id': exercise.id,
        'name': exercise.name,
        'muscle_group': exercise.muscle_group
    }), 201

# ==================== PLAN ROUTES ====================

@app.route('/api/plans', methods=['POST'])
def create_plan():
    """Create a personalized training plan"""
    data = request.get_json()
    user_id = data.get('user_id')

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    plan = Plan(
        user_id=user_id,
        name=f"Plano {user.objective} - {user.level}",
        description=f"Plano personalizado de {user.days_per_week} dias por semana",
        duration_weeks=12
    )

    db.session.add(plan)
    db.session.flush()

    # Create 4 weeks of training sessions
    for week_num in range(1, 5):
        from models import PlanWeek
        plan_week = PlanWeek(plan_id=plan.id, week_number=week_num)
        db.session.add(plan_week)
        db.session.flush()

        # Create training sessions based on user's days per week
        days = list(range(user.days_per_week))
        session_names = ['A', 'B', 'C', 'D', 'E']

        for idx, day in enumerate(days):
            session = TrainingSession(
                plan_week_id=plan_week.id,
                session_name=f"Treino {session_names[idx]}",
                day_of_week=day,
                focus_group=f"Grupo {session_names[idx]}"
            )
            db.session.add(session)

    db.session.commit()

    return jsonify({
        'id': plan.id,
        'name': plan.name,
        'description': plan.description,
        'duration_weeks': plan.duration_weeks
    }), 201

@app.route('/api/plans/<int:plan_id>', methods=['GET'])
def get_plan(plan_id):
    """Get plan details"""
    plan = Plan.query.get(plan_id)

    if not plan:
        return jsonify({'error': 'Plan not found'}), 404

    return jsonify({
        'id': plan.id,
        'name': plan.name,
        'description': plan.description,
        'duration_weeks': plan.duration_weeks,
        'created_at': plan.created_at.isoformat(),
        'weeks': [{
            'week_number': w.week_number,
            'sessions': [{
                'id': s.id,
                'name': s.session_name,
                'focus': s.focus_group,
                'day': s.day_of_week
            } for s in w.sessions]
        } for w in plan.weeks]
    }), 200

@app.route('/api/plans/user/<int:user_id>', methods=['GET'])
def get_user_plans(user_id):
    """Get all plans for a user"""
    plans = Plan.query.filter_by(user_id=user_id).all()

    return jsonify([{
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'duration_weeks': p.duration_weeks,
        'created_at': p.created_at.isoformat(),
        'weeks_count': len(p.weeks)
    } for p in plans]), 200

@app.route('/api/plans/<int:plan_id>', methods=['DELETE'])
def delete_plan(plan_id):
    """Delete a training plan"""
    plan = Plan.query.get(plan_id)

    if not plan:
        return jsonify({'error': 'Plan not found'}), 404

    db.session.delete(plan)
    db.session.commit()

    return jsonify({'message': 'Plan deleted successfully'}), 200

# ==================== WORKOUT ROUTES ====================

@app.route('/api/workouts', methods=['POST'])
def create_workout():
    """Log a completed workout"""
    data = request.get_json()

    workout = Workout(
        user_id=data['user_id'],
        training_session_id=data.get('training_session_id'),
        duration_minutes=data.get('duration_minutes'),
        total_weight=data.get('total_weight'),
        calories_burned=data.get('calories_burned'),
        completed=data.get('completed', True),
        notes=data.get('notes')
    )

    db.session.add(workout)
    db.session.commit()

    # Award points
    user = User.query.get(data['user_id'])
    user.points += 100
    db.session.commit()

    return jsonify({
        'id': workout.id,
        'points_earned': 100,
        'total_points': user.points
    }), 201

@app.route('/api/workouts/<int:user_id>', methods=['GET'])
def get_user_workouts(user_id):
    """Get user's workout history"""
    workouts = Workout.query.filter_by(user_id=user_id).order_by(Workout.date.desc()).all()

    return jsonify([{
        'id': w.id,
        'date': w.date.isoformat(),
        'duration_minutes': w.duration_minutes,
        'total_weight': w.total_weight,
        'calories_burned': w.calories_burned,
        'completed': w.completed
    } for w in workouts]), 200

# ==================== PROGRESS ROUTES ====================

@app.route('/api/progress', methods=['POST'])
def log_progress():
    """Log user progress"""
    data = request.get_json()

    progress = Progress(
        user_id=data['user_id'],
        weight=data.get('weight'),
        body_measurements=data.get('body_measurements'),
        photo_url=data.get('photo_url'),
        notes=data.get('notes')
    )

    db.session.add(progress)
    db.session.commit()

    return jsonify({
        'id': progress.id,
        'date': progress.date.isoformat()
    }), 201

@app.route('/api/progress/<int:user_id>', methods=['GET'])
def get_user_progress(user_id):
    """Get user's progress history"""
    progress_list = Progress.query.filter_by(user_id=user_id).order_by(Progress.date).all()

    return jsonify([{
        'id': p.id,
        'date': p.date.isoformat(),
        'weight': p.weight,
        'measurements': p.body_measurements,
        'photo_url': p.photo_url,
        'notes': p.notes
    } for p in progress_list]), 200

# ==================== MEDAL ROUTES ====================

@app.route('/api/medals/<int:user_id>', methods=['GET'])
def get_user_medals(user_id):
    """Get user's earned medals"""
    medals = Medal.query.filter_by(user_id=user_id).all()

    return jsonify([{
        'id': m.id,
        'name': m.name,
        'icon': m.icon,
        'earned_at': m.earned_at.isoformat()
    } for m in medals]), 200

@app.route('/api/medals', methods=['POST'])
def award_medal():
    """Award a medal to user"""
    data = request.get_json()

    medal = Medal(
        user_id=data['user_id'],
        name=data['name'],
        description=data.get('description'),
        icon=data.get('icon', 'bronze')
    )

    db.session.add(medal)
    db.session.commit()

    return jsonify({
        'id': medal.id,
        'name': medal.name
    }), 201

# ==================== HEALTH CHECK ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Evolua API running'}), 200

# ==================== GAMIFICATION ROUTES ====================

@app.route('/api/gamification/stats/<int:user_id>', methods=['GET'])
def get_gamification_stats(user_id):
    """Get user's gamification stats (points, level, medals, etc)"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    medals = Medal.query.filter_by(user_id=user_id).all()
    total_workouts = Workout.query.filter_by(
        user_id=user_id,
        completed=True
    ).count()

    # Calculate level based on points
    level = (user.points // 500) + 1
    progress_to_next_level = (user.points % 500) / 5

    return jsonify({
        'user_id': user_id,
        'points': user.points,
        'level': level,
        'progress_to_next_level': min(progress_to_next_level, 100),
        'total_workouts': total_workouts,
        'total_medals': len(medals),
        'medals': [{
            'id': m.id,
            'name': m.name,
            'description': m.description,
            'icon': m.icon,
            'earned_at': m.earned_at.isoformat()
        } for m in medals]
    }), 200

@app.route('/api/progress/<int:user_id>/stats', methods=['GET'])
def get_progress_stats(user_id):
    """Get user's progress statistics"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    progress_list = Progress.query.filter_by(user_id=user_id).order_by(Progress.date).all()
    
    return jsonify({
        'weight_progression': [{
            'id': p.id,
            'date': p.date.isoformat(),
            'weight': p.weight,
        } for p in progress_list],
        'summary': {
            'total_workouts': Workout.query.filter_by(user_id=user_id, completed=True).count()
        }
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
