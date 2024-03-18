from flask import Blueprint
from flask_socketio import SocketIO

main_bp = Blueprint('main', __name__)
socketio = SocketIO()

from main import routes
