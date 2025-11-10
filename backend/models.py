from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.dialects.sqlite import JSON

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer)
    objective = db.Column(db.String(50))  # ganho_massa, perda_peso, tonificacao
    level = db.Column(db.String(50))  # iniciante, intermediario, avancado
    days_per_week = db.Column(db.Integer, default=3)
    training_location = db.Column(db.String(50))  # academia, casa, parque
    points = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    plans = db.relationship('Plan', back_populates='user', cascade='all, delete-orphan')
    workouts = db.relationship('Workout', back_populates='user', cascade='all, delete-orphan')
    progress = db.relationship('Progress', back_populates='user', cascade='all, delete-orphan')
    medals = db.relationship('Medal', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.name}>'

class Plan(db.Model):
    __tablename__ = 'plans'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    duration_weeks = db.Column(db.Integer, default=12)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='plans')
    weeks = db.relationship('PlanWeek', back_populates='plan', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Plan {self.name}>'

class PlanWeek(db.Model):
    __tablename__ = 'plan_weeks'

    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.id'), nullable=False)
    week_number = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    plan = db.relationship('Plan', back_populates='weeks')
    sessions = db.relationship('TrainingSession', back_populates='week', cascade='all, delete-orphan')

class TrainingSession(db.Model):
    __tablename__ = 'training_sessions'

    id = db.Column(db.Integer, primary_key=True)
    plan_week_id = db.Column(db.Integer, db.ForeignKey('plan_weeks.id'), nullable=False)
    session_name = db.Column(db.String(120))  # Treino A, B, C, etc
    day_of_week = db.Column(db.Integer)  # 0=Monday, 6=Sunday
    focus_group = db.Column(db.String(120))  # Peito/Costas, Perna, Braço, etc
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    week = db.relationship('PlanWeek', back_populates='sessions')
    exercises = db.relationship('SessionExercise', back_populates='session', cascade='all, delete-orphan')

class SessionExercise(db.Model):
    __tablename__ = 'session_exercises'

    id = db.Column(db.Integer, primary_key=True)
    training_session_id = db.Column(db.Integer, db.ForeignKey('training_sessions.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    sets = db.Column(db.Integer, default=3)
    reps = db.Column(db.String(50))  # "8-10", "12-15", etc
    rest_seconds = db.Column(db.Integer, default=60)
    order = db.Column(db.Integer)

    # Relationships
    session = db.relationship('TrainingSession', back_populates='exercises')
    exercise = db.relationship('Exercise', back_populates='sessions')

class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text)
    muscle_group = db.Column(db.String(120))  # Peito, Costas, Perna, Braço, etc
    difficulty = db.Column(db.String(50))  # Iniciante, Intermediario, Avançado
    video_url = db.Column(db.String(500))
    instructions = db.Column(db.Text)
    safety_tips = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    sessions = db.relationship('SessionExercise', back_populates='exercise')

    def __repr__(self):
        return f'<Exercise {self.name}>'

class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    training_session_id = db.Column(db.Integer, db.ForeignKey('training_sessions.id'))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    duration_minutes = db.Column(db.Integer)
    total_weight = db.Column(db.Float)  # Total weight lifted
    calories_burned = db.Column(db.Float)
    completed = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)

    # Relationships
    user = db.relationship('User', back_populates='workouts')
    exercises_log = db.relationship('ExerciseLog', back_populates='workout', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Workout {self.date}>'

class ExerciseLog(db.Model):
    __tablename__ = 'exercise_logs'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    sets_completed = db.Column(db.Integer)
    actual_reps = db.Column(db.JSON)  # [10, 10, 9] - reps per set
    weight_per_set = db.Column(db.JSON)  # [20, 20, 20] - kg per set
    difficulty_feedback = db.Column(db.String(50))  # facil, normal, dificil
    completed = db.Column(db.Boolean, default=False)

    # Relationships
    workout = db.relationship('Workout', back_populates='exercises_log')
    exercise = db.relationship('Exercise')

class Progress(db.Model):
    __tablename__ = 'progress'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    weight = db.Column(db.Float)
    body_measurements = db.Column(db.JSON)  # {"chest": 100, "waist": 80, ...}
    photo_url = db.Column(db.String(500))
    notes = db.Column(db.Text)

    # Relationships
    user = db.relationship('User', back_populates='progress')

    def __repr__(self):
        return f'<Progress {self.date}>'

class Medal(db.Model):
    __tablename__ = 'medals'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))  # bronze, silver, gold, etc
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='medals')

    def __repr__(self):
        return f'<Medal {self.name}>'
