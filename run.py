from flask_migrate import Migrate
from app import create_app, db
from app.models.user import User
from app.models.order import Order

app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # This will create the tables if they don't exist
    app.run(debug=True)