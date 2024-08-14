from flask import Flask

# Create the Flask application
app = Flask(__name__)

# Import the endpoints
from api.endpoints.accounts import *

if __name__ == "__main__":
    app.run(debug=True)
