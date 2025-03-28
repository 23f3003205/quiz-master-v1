import os
from flask import Flask
# from flask_wtf.csrf import CSRFProtect
from models.model import db
from controllers.auth import auth_bp
from controllers.admin import admin_bp
from controllers.user import user_bp

app = Flask(__name__)

# Ensure the database directory exists
if not os.path.exists('db_directory'):
    os.makedirs('db_directory')

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///db_directory/quiz_db.sqlite3')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')

# # Initialize CSRF protection
# csrf = CSRFProtect(app)

# Initialize database
db.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(user_bp, url_prefix='/user')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

