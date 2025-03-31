from app import create_app, db
from app.models import Book, Review  # Import your models
from dotenv import load_dotenv

app = create_app()
load_dotenv() # Load environment variables

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
