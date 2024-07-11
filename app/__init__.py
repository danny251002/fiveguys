from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.views import main, auth, manager, worker, customer
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(manager.bp)
    app.register_blueprint(worker.bp)
    app.register_blueprint(customer.bp)

    from app.models.user import User
    from app.models.menu_item import MenuItem
    from app.models.order import Order, OrderItem, CartItem

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app