from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.model import db, Subject, Chapter, Quiz,Questions


admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
def dashboard():
    field='Quiz'
    visitor='admin'
    subjects= Subject.query.all()  # Fetch all subjects
    return render_template('admin_dashboard/admin_dashboard.html',field=field,visitor=visitor,subjects=subjects)

@admin_bp.route('/add-subject', methods=['GET', 'POST'])
def add_subject():
    if request.method == 'POST':
        sub_name = request.form['sub_name']
        description = request.form['description']
        new_subject = Subject(sub_name=sub_name, description=description)
        db.session.add(new_subject)
        db.session.commit()
        flash('New Subject Added!', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin_dashboard/add_new_subject.html')

@admin_bp.route('/add-chapter', methods=['GET', 'POST'])
def add_chapter():
    if request.method == 'POST':
        subject_id = request.form['subject_id']
        name = request.form['chapter_name']
        no_questions = request.form['no_questions']
        new_chapter = Chapter(subject_id=subject_id, name=name, no_questions=no_questions)
        db.session.add(new_chapter)
        db.session.commit()
        flash('New Chapter Added!', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin_dashboard/add_new_chapter.html')

# Edit Chapter
@admin_bp.route('/quiz-management/<int:chapter_id>', methods=['GET', 'POST'])
def quiz_management(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)  # Fetch the chapter or return 404 if not found
    quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()  # Fetch all quizzes for this chapter
    return render_template('admin_dashboard/quiz_management.html', chapter=chapter, quizzes=quizzes)

# Delete Chapter
@admin_bp.route('/delete-chapter/<int:chapter_id>', methods=['POST'])
def delete_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)  # Fetch the chapter or return 404 if not found
    # Delete all quizzes and questions related to this chapter
    Quiz.query.filter_by(chapter_id=chapter_id).delete()
    db.session.delete(chapter)
    db.session.commit()
    flash('Chapter and related quiz deleted successfully!', 'success')
    return redirect(url_for('admin.dashboard'))


# 🎯 Add New Quiz
@admin_bp.route('/add-quiz', methods=['GET', 'POST'])
def add_quiz():
    if request.method == 'POST':
        chapter_id = request.form['chapter_id']
        duration = request.form['duration']
        date = request.form['date']
        new_quiz = Quiz(chapter_id=chapter_id, duration=duration,date=date)
        
        
        db.session.add(new_quiz)
        db.session.commit()
        
        flash('New Quiz Added Successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    
    chapters = Chapter.query.all()  # Fetch all chapters
    return render_template('admin_dashboard/addNew_Quiz.html', chapters=chapters)

# 📝 Add New Question to a Quiz
@admin_bp.route('/add-question', methods=['GET', 'POST'])
def add_question(quiz_id):
    if request.method == 'POST':
        quiz_id = quiz_id
        title = request.form['title']
        statement = request.form['statement']
        option_a = request.form['option_a']
        option_b = request.form['option_b']
        option_c = request.form['option_c']
        option_d = request.form['option_d']
        correct_option = request.form['correct_option']

        new_question = Questions(
            quiz_id=quiz_id, que_title=title, que_statement=statement,
            option_1=option_a, option_2=option_b, 
            option_3=option_c, option_4=option_d,
            correct_option=correct_option
        )
        
        db.session.add(new_question)
        db.session.commit()
        
        flash('New Question Added!', 'success')
        return redirect(url_for('admin.dashboard'))
    
    quizzes = Quiz.query.all()  # Fetch all quizzes
    return render_template('admin_dashboard/addNew_question.html', quizzes=quizzes)

@admin_bp.route('/delete-quiz/<int:quiz_id>', methods=['POST'])
def delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)

    # Delete all questions linked to this quiz first
    Questions.query.filter_by(quiz_id=quiz_id).delete()

    # Delete the quiz itself
    db.session.delete(quiz)
    db.session.commit()
    
    flash('Quiz deleted successfully!', 'success')
    return redirect(url_for('admin.quiz_management'))

