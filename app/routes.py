from app import app, db
from .models import User, Company, AIIdea, Entry
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, EditProfileForm, CompanyRegistrationForm, ModelIdeaForm, HairTransForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from .service import AIService


@app.route('/')
@app.route('/index')
def index():
    context = {'service': 'Hair Transplant',
               'call': 'Check it on the bar above'}
    return render_template('index.html', title='Home', context=context)


@app.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congrats, you are now a registered user')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/comp_register', methods=['GET', 'POST'])
def comp_register():
    if current_user.is_authenticated and current_user.company_id is not None:
        company = Company.query.filter_by(id=current_user.company_id).first()
        flash('You already belong to company {}'.format(company.name))
        return redirect(url_for('index'))
    form = CompanyRegistrationForm()
    if form.validate_on_submit():
        company = Company(name=form.name.data, contact=form.contact.data)
        db.session.add(company)
        db.session.flush()
        current_user.company_id = company.id
        db.session.commit()
        flash('Company saved')
        return redirect(url_for('index'))  # This should redirect to company page
    return render_template('company.html', title='Company', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/users/', methods=['GET'])
def get_users():
    users = User.query.all()
    return users


@app.route('/user/<username>')
@login_required
def user_details(username):
    user = User.query.filter_by(username=username).first_or_404()
    # company = Company.query.filter_by(id=user.company_id).first_or_404()
    # data = {
    #     'user': user,
    #     'company': company,
    # }
    return render_template('user.html', user=user)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash('You changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@app.route('/model_idea', methods=['GET', 'POST'])
def model_idea():
    if current_user.is_anonymous:
        flash('You need to login to leave a model suggestion.')
        return redirect(url_for('index'))
    form = ModelIdeaForm()
    if form.validate_on_submit():
        idea = AIIdea(user_id=current_user.id,
                      name=form.name.data,
                      category=form.category.data,
                      description=form.description.data)
        db.session.add(idea)
        db.session.commit()
        flash('Your idea has been submitted we will contact you as soon as possible.')
        return redirect(url_for('index'))
    return render_template('model_idea.html', title='Model Idea', form=form)


@app.route('/api_docs', methods=['GET', 'POST'])
def api_docs():
    return render_template('api_docs', title='API documentation')


@app.route('/service/hair_trans', methods=['GET', 'POST'])
def hair_trans():
    if current_user.is_anonymous:
        flash('Please sign in to try out services.')
        return redirect(url_for('index'))
    form = HairTransForm()
    if form.validate_on_submit():
        user = current_user.id
        image = request.files['image']
        data = image.read()

        work_dict = {'user': user,
                     'image': data}
        service = AIService.hair_transplant_service(work_dict)
        print(service)

        return render_template('hair_transplant_result.html', form=form, context=service)
    return render_template('hair_transplant.html', title='Hair Transplant Model', form=form)


@app.route('/service/results', methods=['GET'])
def get_service_result():
    if current_user.is_anonymous:
        flash('Please sign in to try out services.')
        return redirect(url_for('index'))

    import base64
    from io import BytesIO
    entry = Entry.query.filter_by(user_id=current_user.id).order_by(Entry.created.desc()).first()

    binary_string = bytes(entry.image)
    base64_string = base64.b64encode(binary_string).decode('utf-8')

    context = {'image': base64_string,
               'user': 'Ira'}
    return render_template('hair_transplant_result.html', context=context)





