from . import chess_bp
from flask import render_template, request, redirect, url_for, flash, session
from flask import current_app as app
from flask_login import current_user, login_user, logout_user, login_required,LoginManager
from flask_socketio import send, emit,SocketIO,join_room
from .. import socketio
from ChessApp.db import User,Game
import json
login_manager = LoginManager(app)
login_manager.login_view = "user_bp.login"
login_manager.login_message = "You cannot access this page. Please login"
from mongoengine.queryset.visitor import Q

@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=session["username"]).first()

users={}
@chess_bp.route('/')
def index():
  return render_template('chess.html')

@chess_bp.route('/<room>')
@login_required
def play(room):
  print(room)
  game = Game.objects(room=room).first()
  if User.objects(username=session['username']).first() == game['whitePlayer']:
    print("White")
    return render_template('chess.html',player=json.loads(game.to_json()))
  if User.objects(username=session['username']).first() == game['blackPlayer']:
    print("Black")
    return render_template('chess.html',player=json.loads(game.to_json()))

@socketio.on('connect')
def connect():
  print("Socket Connected")

@socketio.on('join_room')
def join_room(data):
    global users
    users[session['username']] = request.sid
    print(users)
    print(data)
    # join_room(data['room'])
    game = Game.objects(room=data['room']).first()
    if User.objects(username=session['username']).first() == game['whitePlayer']:
      print("White")
      emit('user_connect', {'data' : 'user connected','color':'white'},to=users[session['username']])
    elif User.objects(username=session['username']).first() == game['blackPlayer']:
      print("Black")
      emit('user_connect', {'data' : 'user connected','color':'black'})
  
@socketio.on('move')
def handle_move(msg):
    global users
    print(users)
    print(msg)
    print(msg['room'])
    game = Game.objects(room=msg['room']).first()
    game.update(fen=msg['fen'])
    game.update(pgn=msg['pgn'])
    print("MOVE",msg['whos_move'])
    emit('move', {'move':msg},broadcast=True)

@socketio.on('gameOver')
def gameOver(msg):
    global users
    print(users)
    print(msg)
    print(msg['room'])
    game = Game.objects(room=msg['room']).first()
    if msg['loser'] == 'Black':
      game.update(winner=game['whitePlayer'])
      game['whitePlayer'].update(totalWins=game['whitePlayer']['totalWins']+1)
      game['whitePlayer'].update(totalPoints=game['whitePlayer']['totalPoints']+2)
    else:
      game.update(winner=game['blackPlayer'])
      game.update(winner=game['blackPlayer'])
      game['blackPlayer'].update(totalWins=game['blackPlayer']['totalWins']+1)
      game['blackPlayer'].update(totalPoints=game['blackPlayer']['totalPoints']+2)
    game.update(fen=msg['fen'])
    game.update(pgn=msg['pgn'])
    print("MOVE",msg['whos_move'])
    return redirect(url_for('user_bp.index'))