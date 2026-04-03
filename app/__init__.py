from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_socketio import SocketIO
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
socketio = SocketIO(cors_allowed_origins="*")

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    socketio.init_app(app)

    # Blueprints
    from app.routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.routes.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.routes.doctor import bp as doctor_bp
    app.register_blueprint(doctor_bp, url_prefix='/doctors')

    from app.routes.chat import bp as chat_bp
    app.register_blueprint(chat_bp, url_prefix='/chat')

    # Google verification route
    @app.route('/googlec158ac2d82043b05.html')
    def google_verify():
        return "google-site-verification: googlec158ac2d82043b05.html"

    # Optional home route
    @app.route('/')
    def home():
        return "Sayt ishlayapti ✅"

    return app

from app import models