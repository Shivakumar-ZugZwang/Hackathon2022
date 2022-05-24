from . import user_bp
from flask import render_template, request, redirect, url_for, flash, session,current_app
from flask_login import login_user,LoginManager, logout_user, login_required, current_user
from flask import current_app as app

from ChessApp.db import User,Game
from flask_mail import Message, Mail

login_manager = LoginManager(app)
login_manager.login_view = "user_bp.login"
login_manager.login_message = "You cannot access this page. Please login"

@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=session["username"]).first()


@user_bp.route('/')
def index():
    if session.get("username"):
        user = User.objects(username__nin=[session["username"]])
        d = []
        for i in user:
            if i.is_authenticated:
                d.append(i)

        return render_template('index.html',user=d)
    else:
        return render_template('index.html')
  
@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.objects(email=email).first()
        if user and user.get_password(password):
            session['username'] = user['username']
            login_user(user)
            flash('You are now logged in.')
            return redirect(url_for('user_bp.index'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html')

@user_bp.route('/register',methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']
        if password != confirm:
            print("Password Mismatch")
            flash('Passwords do not match','danger')
            return redirect(url_for('user_bp.register'))
        else:
            user = User()
            user.username = username
            user.email = email
            user.set_password(password)
            user.save()
            flash('User created successfully','success')
            return redirect(url_for('user_bp.login'))
        
    return render_template('register.html')

@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('username',None)
    flash('You are now logged out.')
    return redirect(url_for('user_bp.index'))

@user_bp.route('/play<username>')
@login_required
def play(username):
    user = User.objects(username=username).first()
    print(user['username'])
    room = session['username']+user['username']
    if not Game.objects(room=room).first():
        game = Game()
        game.whitePlayer = User.objects(username=session['username']).first()
        game.blackPlayer = User.objects(username=user['username']).first()
        game.room = session['username']+user['username']
        game.save()
    app = current_app._get_current_object()
    mail = Mail(app)
    message = Message(
        subject="CodeVerse Chess Notification",
        sender="mail.cvchess@gmail.com",
        recipients=[user['email']]
    )
    # link = url_for("chess_bp.play", _external=True)
    # link +='/'+room
    message.body = """{} wants to Play Chess with you...

    Click link to open Board and Play
    http://127.0.0.1:5000/chess/play{}""".format(session['username'],room)
    mail.send(message)
    return redirect(url_for('chess_bp.play',room=room)) 

@user_bp.route('/leaderBoard')
def leaderBoard():
    # user = User.objects(username=session['username']).first()
    users = User.objects()
    return render_template('leaderBoard.html',users=users)