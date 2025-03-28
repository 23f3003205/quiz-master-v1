from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    fullname = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String, nullable=True)
    role = db.Column(db.String(10), nullable=False, default='user')  # 'admin' or 'user'

class Subject(db.Model):
    __tablename__ = 'subject'
    id = db.Column(db.Integer, primary_key=True)
    sub_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String, nullable=True)
    chapters = db.relationship('Chapter', backref='subject', lazy=True)

class Chapter(db.Model):
    __tablename__ = 'chapter'
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    no_questions = db.Column(db.Integer, nullable=False)
    quizzes = db.relationship('Quiz', backref='chapter', lazy=True)

class Quiz(db.Model):
    __tablename__ = 'quiz'
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    date = db.Column(db.String, nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # in minutes
    questions = db.relationship('Questions', backref='quiz', lazy=True)

class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    que_statement = db.Column(db.Text, nullable=False)
    que_title = db.Column(db.String(255), nullable=False)
    options_1 = db.Column(db.Text, nullable=False) 
    options_2 = db.Column(db.Text, nullable=False)
    options_3 = db.Column(db.Text, nullable=False)
    options_4 = db.Column(db.Text, nullable=False)
    correct_option = db.Column(db.String(100), nullable=False)

class Score(db.Model):
    __tablename__ = 'score'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), primary_key=True, nullable=False)
    total_scored = db.Column(db.Integer, nullable=False)
