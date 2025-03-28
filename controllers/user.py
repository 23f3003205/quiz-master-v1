from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from models.model import db, Quiz, Score

user_bp = Blueprint('user', __name__)

@user_bp.route('/dashboard')
def dashboard():
    return render_template('user_dashboard/user_dashboard.html')

@user_bp.route('/quiz/start/<int:quiz_id>')
def start_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        flash("Quiz not found!", "danger")
        return redirect(url_for('user.dashboard'))
    
    return render_template('user_dashboard/quiz_start.html', quiz=quiz)

@user_bp.route('/quiz/submit', methods=['POST'])
def submit_quiz():
    user_id = session.get('user_id')
    quiz_id = request.form['quiz_id']
    total_score = request.form['total_score']

    new_score = Score(user_id=user_id, quiz_id=quiz_id, total_scored=total_score)
    db.session.add(new_score)
    db.session.commit()

    flash("Quiz submitted successfully!", "success")
    return redirect(url_for('user.dashboard'))
