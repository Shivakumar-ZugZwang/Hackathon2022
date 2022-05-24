from flask import Flask
from flask_socketio import SocketIO
from os import urandom

socketio = SocketIO(
  async_mode='gevent',
  
)

def create_app():
  app = Flask(__name__)
  socketio.init_app(app)
  app.config['SECRET_KEY'] = urandom(16)
  app.config['MAIL_SERVER'] = 'smtp.gmail.com'
  app.config['MAIL_PORT'] = 465
  app.config['MAIL_USERNAME'] = "mail.cvchess@gmail.com"
  app.config['MAIL_PASSWORD'] = "Cscode123"
  app.config['MAIL_USE_SSL'] = True

  app.config['SECRET_KEY'] = 'secret!'
  with app.app_context():
    from .User import user
    from .Chess import chess

    app.register_blueprint(user.user_bp)
    app.register_blueprint(chess.chess_bp)
  return app,socketio