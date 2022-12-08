from app import app
from .models import User


@app.route('/')
@app.route('/index')
def index():
    return "Fideri"


@app.route('/plebs/')
def plebs():
    return 'ti si fider!'


@app.route('/users/', methods=['GET'])
def get_users():
    user = User(username='Oliver', password='feeding')
    result = {"username": user.username,
              "password": user.password}
    return result
