from flask import Blueprint
chess_bp = Blueprint('chess_bp',__name__,url_prefix='/chess',template_folder="templates",static_folder="static")