from flask import Flask, render_template, url_for, request, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
from models import user as user_model
from models import friends as friends_model
from models import Notification as Notifications_model

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

friends = friends_model.Friends_(db)
notifications = Notifications_model.Notification_(db)
User = user_model.User_(db, friends, notifications)
