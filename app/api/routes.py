from flask import Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from flask_restful import Api, Resource, url_for

api_bp = Blueprint('api', __name__, url_prefix='/api/v0.1')
api = Api(api_bp)


# @api_bp.route('/get_data')
# @login_required

class Data(Resource):
    def get(self):
        return {'key': 'value',
                'Ira': 'Eng',
                'Darkness': 'Old friend',
                '21p': 'chlorine'}

    def post(self):
        return {'data': 'taken'}


@api_bp.route('/hi')
def hi():
    return "hi!"


api.add_resource(Data, '/data')
