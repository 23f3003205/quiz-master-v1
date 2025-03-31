from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.model import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['user_id'] = user.id  # Store user_id in session
            session['role'] = user.role
            flash('Login successful!', 'success')
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))  # Matches '/admin/dashboard'
            else:
                return redirect(url_for('user.dashboard'))  # Matches '/user/dashboard'
        else:
            flash('Invalid username or password', 'danger')

    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        fullname = request.form['fullname']
        dob = request.form['dob']

        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'danger')
        else:
            new_user = User(username=username, password=password, fullname=fullname, dob=dob)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created! Please log in.', 'success')
            return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'info')
    return redirect(url_for('auth.login'))
