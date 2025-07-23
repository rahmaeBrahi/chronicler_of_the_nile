from src.main import app
from src.models.conversation import db

with app.app_context():
    db.create_all()
    print("Database initialized.")

