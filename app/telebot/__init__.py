from flask import Blueprint

bp = Blueprint('telebot', __name__)

from app.telebot import routes
