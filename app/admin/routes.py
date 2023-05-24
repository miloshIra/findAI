from flask import Blueprint, render_template
from .models import Dashboard
from flask_login import ( current_user, 
                        login_user,
                        logout_user, login_required )

from app.decorators import role_required


admin_bp = Blueprint('admin', __name__,
                      template_folder='templates', url_prefix='/admin')


@admin_bp.before_request
@login_required
@role_required('admin')
def before_request():
    """ Protects admin endpoints """
    pass

# Dashboard --------------------------------------------------------------------
@admin_bp.route('', methods=["GET", "POST"])
def dashboard():
    group_and_count_users = Dashboard.group_and_count_users()
    return render_template('dashboard.html', group_and_count_users=group_and_count_users)



