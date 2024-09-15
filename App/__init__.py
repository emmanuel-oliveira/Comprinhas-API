import os

from dotenv import load_dotenv
from flask import Flask
#from flask_cors import CORS


load_dotenv()

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
#cors = CORS(app)

app.environment = os.getenv("FLASK_ENVIRONMENT", "dev")

from .Routes import Routes