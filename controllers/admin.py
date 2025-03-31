from flask import Blueprint, render_template, request, redirect, url_for, flash,session
from models.model import db, Subject, Chapter,Questions


admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
def dashboard():
    
    subjects= Subject.query.all()  # Fetch all subjects
    return render_template('admin_dashboard/admin_dashboard.html',subjects=subjects)

@admin_bp.route('/add-subject', methods=['GET', 'POST'])
def add_subject():
    if request.method == 'POST':
        sub_name = request.form['sub_name']
        description = request.form['description']
        new_subject = Subject(sub_name=sub_name, description=description)
        db.session.add(new_subject)
        db.session.commit()
        # flash('New Subject Added!', 'success')
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

    #For GET request, retrieve subject_id from the URL
    subject_id = request.args.get('subject_id')
    return render_template('admin_dashboard/add_new_chapter.html',subject_id=subject_id)

@admin_bp.route('/edit-chapter/<int:chapter_id>', methods=['GET', 'POST'])
def edit_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)  # Fetch the chapter or return 404 if not found

    if request.method == 'POST':
        # Update the chapter details from the form
        chapter.name = request.form['name']
        chapter.no_questions = request.form['no_questions']

        db.session.commit()  # Save the changes to the database
        flash('Chapter updated successfully!', 'success')

        # Redirect back to the admin dashboard
        return redirect(url_for('admin.dashboard'))

    # Render the edit chapter form with the current chapter details
    return render_template('admin_dashboard/edit_chapter.html', chapter=chapter)


# Edit Chapter
@admin_bp.route('/quiz-management', methods=['GET', 'POST'])
def quiz_management():
    chapters=Chapter.query.all() # Fetch all quizzes for the chapter
    return render_template('admin_dashboard/quiz_management.html',chapters=chapters)

# Delete Chapter
@admin_bp.route('/delete-chapter/<int:chapter_id>', methods=['POST'])
def delete_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)  # Fetch the chapter or return 404 if not found
    db.session.delete(chapter)
    db.session.commit()
    flash('Chapter and related quiz deleted successfully!', 'success')
    return redirect(url_for('admin.dashboard'))



# 📝 Add New Question to a Quiz
@admin_bp.route('/add-question/<int:chapter_id>`', methods=['GET', 'POST'])
def add_question(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)

    if request.method == 'POST':
        # Retrieve form data
        que_statement = request.form['que_statement']
        que_title = request.form['que_title']
        option_1 = request.form['option_1']
        option_2 = request.form['option_2']
        option_3 = request.form['option_3']
        option_4 = request.form['option_4']
        correct_option = request.form['correct_option']

        # Calculate the next question_number for the chapter
        max_question_number = db.session.query(db.func.max(Questions.question_number)).filter_by(chapter_id=chapter_id).scalar()
        next_question_number = (max_question_number or 0) + 1

        # Create a new question
        new_question = Questions(
            chapter_id=chapter_id,
            question_number=next_question_number,
            que_statement=que_statement,
            que_title=que_title,
            option_1=option_1,
            option_2=option_2,
            option_3=option_3,
            option_4=option_4,
            correct_option=correct_option
        )

        # Add to the database
        db.session.add(new_question)
        db.session.commit()

        flash('Question added successfully!', 'success')
        return redirect(url_for('admin.quiz_management', chapter_id=chapter_id))

    return render_template('admin_dashboard/add_question.html', chapter=chapter)

@admin_bp.route('/edit-question/<int:chapter_id>/<int:question_number>', methods=['GET', 'POST'])
def edit_question(chapter_id, question_number):
    # Fetch the question using both chapter_id and question_number
    question = Questions.query.filter_by(chapter_id=chapter_id, question_number=question_number).first_or_404()

    if request.method == 'POST':
        # Update the question details from the form
        question.que_title = request.form['que_title']
        question.que_statement = request.form['que_statement']
        question.option_1 = request.form['option_1']
        question.option_2 = request.form['option_2']
        question.option_3 = request.form['option_3']
        question.option_4 = request.form['option_4']
        question.correct_option = request.form['correct_option']

        db.session.commit()  # Save the changes to the database
        flash('Question updated successfully!', 'success')

        # Redirect back to the quiz management page
        return redirect(url_for('admin.quiz_management'))

    return render_template('admin_dashboard/edit_question.html', question=question)

@admin_bp.route('/delete-question/<int:chapter_id>/<int:question_number>', methods=['POST'])
def delete_question(chapter_id, question_number):
    question = Questions.query.filter_by(chapter_id=chapter_id, question_number=question_number).first_or_404()

    db.session.delete(question)  # Delete the question
    db.session.commit()  # Commit the deletion to the database

    # Re-sequence question numbers for the chapter
    subsequent_questions = Questions.query.filter(
        Questions.chapter_id == chapter_id,
        Questions.question_number > question_number
    ).order_by(Questions.question_number).all()

    for q in subsequent_questions:
        q.question_number -= 1  # Decrement the question number
    db.session.commit()  # Commit the re-sequencing changes

    flash('Question deleted successfully and sequence updated!', 'success')
    return redirect(url_for('admin.quiz_management'))

@admin_bp.route('/logout', methods=['GET'])
def logout():
    # Clear the session or perform any logout logic
    session.clear()
    flash('You have been logged out successfully!', 'success')
    return redirect(url_for('auth.login'))  # Redirect to the login page

