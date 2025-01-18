from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from dotenv import load_dotenv
import os
# importing packages 

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
socket = SocketIO(app)
cors = CORS(socket)
# configuring application 


# blueprints 

if __name__ == '__main__':
    socket.run(app, debug=True)