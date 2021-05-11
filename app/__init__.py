from flask import Flask
from whitenoise import WhiteNoise

app = Flask(__name__, static_folder='static')
app.config.from_object('config.DevelopmentConfig')
app.wsgi_app = WhiteNoise(app.wsgi_app, root='app/static/')

from app import views, login_views, admin_views
