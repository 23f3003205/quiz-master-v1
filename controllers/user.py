from flask import Blueprint, render_template, request, session, redirect, url_for, flash, current_app
from models.model import db, Chapter, Score, Questions
from controllers.auth import auth_bp  # Ensure auth blueprint is imported

user_bp = Blueprint('user', __name__)

@user_bp.route('/dashboard')
def dashboard():
    chapters = Chapter.query.all()
    return render_template('user_dashboard/user_dashboard.html', chapters=chapters)

@user_bp.route('/start-quiz/<int:chapter_id>', methods=['GET', 'POST'])
def start_quiz(chapter_id):
   
    if 'user_id' not in session:
        # Forbidden: User is not logged in
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('auth.login'))
    
    questions = Questions.query.filter_by(chapter_id=chapter_id).all()
    if not questions:  # Handle empty questions list
        flash('No questions available for this chapter.', 'warning')
        return redirect(url_for('user.dashboard'))
    
    if request.method == 'POST':
        answers = request.form.to_dict()  # Get all form data as a dictionary
        print(answers) 
        print(answers.get('1_1', 'N/A'))  # Debugging line to check the answers received
        score = 0
        # total_que=len(questions)
        for question in questions:
            user_answer = answers.get(f"{chapter_id}_{question.question_number}", None)
            print(f"user_answer:{user_answer}")
            correct_answer = question.correct_option
            print(f"correct_answer:{correct_answer}")
            if user_answer and user_answer == correct_answer:
                score += 1
                print(score)
        
        print(f"Score: {score}")  # Debugging line to check the score calculated
        
        
        try:
            # Store score in the database
            attempt_number = Score.query.filter_by(user_id=session['user_id'], chapter_id=chapter_id).count() + 1
            new_score = Score(user_id=session['user_id'], chapter_id=chapter_id, attempt_number=attempt_number, total_scored=score)
            db.session.add(new_score)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            
            flash('An error occurred while saving your score. Please try again.', 'danger')
            return render_template('user_dashboard/quiz_start.html', questions=questions, chapter_id=chapter_id, answers=answers)

        return redirect(url_for('user.user_scores'))
    
    return render_template('user_dashboard/quiz_start.html', questions=questions, chapter_id=chapter_id)

@user_bp.route('/user-scores', methods=['GET'])
def user_scores():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to view your scores.', 'warning')
        return redirect(url_for('auth.login'))
    
    scores = Score.query.filter_by(user_id=user_id).all()
    if not scores:
        flash('No scores available.', 'info')
        return redirect(url_for('user.dashboard'))
    
    return render_template('user_dashboard/user_score.html', scores=scores)
    

@user_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))  # Ensure 'auth' blueprint is registered
