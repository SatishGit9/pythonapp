
from app import app, init_db
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == '__main__':
    # Initialize the database
    init_db()
    
    # Run the application
    app.run(
        host=os.getenv('HOST', '0.0.0.0'),
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('FLASK_DEBUG', 'False') == 'True'
    )
