from app import app


@app.route('/')
@app.route('/index')
def index():
    return "Fideri"


@app.route('/plebs/')
def plebs():
    return 'ti si fider!'

