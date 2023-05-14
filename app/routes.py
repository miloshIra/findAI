from app import app, db
from .models import User, Company, ModelIdea, Entry
from flask import render_template, flash, redirect, url_for, request, jsonify
from app.forms import LoginForm, RegistrationForm, EditProfileForm, CompanyRegistrationForm, \
                      ModelIdeaForm, HairTransForm, WeightLossForm, MuscleGainForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from .service import AIService
import base64


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
    entries = Entry.query.filter_by(user_id=user.id).order_by(Entry.created.desc()).limit(5).all()
    company = Company.query.filter_by(id=user.company_id).first_or_404()

    for entry in entries:
        entry.image = base64.b64encode(bytes(entry.image)).decode(('utf-8'))
        # entry.image = entry
        # base64_image_string = base64.b64encode(binary_image_string).decode('utf-8')
        # entry = base64_image_string

    context = {
            'user': user,
            'company': company,
            'entries': entries}

    return render_template('user.html', user=user, context=context)


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
        idea = ModelIdea(user_id=current_user.id,
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


@app.route('/products', methods=["GET"])
def products():
    entry_hair_transplant = Entry.query.filter_by(service='hair_transplant').first_or_404()
    entry_muscle_gain = Entry.query.filter_by(service='muscle_gain').first_or_404()
    entry_weight_loss = Entry.query.filter_by(service='weight_loss').first_or_404()

    ht_binary_image_string = bytes(entry_hair_transplant.image)
    ht_base64_image_string = base64.b64encode(ht_binary_image_string).decode('utf-8')

    mg_binary_image_string = bytes(entry_muscle_gain.image)
    mg_base64_image_string = base64.b64encode(mg_binary_image_string).decode('utf-8')

    wl_binary_image_string = bytes(entry_weight_loss.image)
    wl_base64_image_string = base64.b64encode(wl_binary_image_string).decode('utf-8')

    context = {'ht_image': ht_base64_image_string,
               'wl_image': wl_base64_image_string,
               'mg_image': mg_base64_image_string,
               'user': 'Ira'}

    return render_template('products.html', context=context)


@app.route('/docs', methods=["GET"])
def docs():
    return render_template('docs.html')


@app.route('/pricing', methods=["GET"])
def pricing():
    return render_template('pricing.html')


@app.route('/product/hair_trans', methods=['GET', 'POST'])
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

        AIService.hair_transplant_service(work_dict)

        return redirect(url_for('hair_transplant_result'))
    return render_template('hair_transplant.html', title='Hair Transplant Model', form=form)


@app.route('/product/hair_transplant_results', methods=['GET'])
def hair_transplant_result():
    if current_user.is_anonymous:
        flash('Please sign in to try out services.')
        return redirect(url_for('index'))

    entry = Entry.query.filter_by(user_id=current_user.id).order_by(Entry.created.desc()).first()

    binary_image_string = bytes(entry.image)
    base64_image_string = base64.b64encode(binary_image_string).decode('utf-8')

    context = {'image': base64_image_string,
               'user': 'Ira'}

    return render_template('hair_transplant_result.html', context=context)


@app.route('/product/weight_loss', methods=['GET', 'POST'])
def weight_loss():
    if current_user.is_anonymous:
        flash('Please sign in to try out services.')
        return redirect(url_for('index'))
    form = WeightLossForm()
    if form.validate_on_submit():
        user = current_user.id
        image = request.files['image']
        data = image.read()

        work_dict = {'user': user,
                     'image': data}

        AIService.weight_loss_service(work_dict)

        return redirect(url_for('weight_loss_result'))
    return render_template('weight_loss.html', title='Weight Loss Model', form=form)


@app.route('/product/weight_loss_results', methods=['GET'])
def weight_loss_result():
    if current_user.is_anonymous:
        flash('Please sign in to try out services.')
        return redirect(url_for('index'))

    entry = Entry.query.filter_by(user_id=current_user.id).order_by(Entry.created.desc()).first()

    binary_image_string = bytes(entry.image)
    base64_image_string = base64.b64encode(binary_image_string).decode('utf-8')

    context = {'image': base64_image_string,
               'user': 'Ira'}

    return render_template('weight_loss_result.html', context=context)


@app.route('/product/muscle_gain', methods=['GET', 'POST'])
def muscle_gain():
    if current_user.is_anonymous:
        flash('Please sign in to try out services.')
        return redirect(url_for('index'))
    form = MuscleGainForm()
    if form.validate_on_submit():
        user = current_user.id
        image = request.files['image']
        data = image.read()

        work_dict = {'user': user,
                     'image': data}

        AIService.muscle_gain_service(work_dict)

        return redirect(url_for('muscle_gain_result'))
    return render_template('muscle_gain.html', title='Muscle Gain Model', form=form)


@app.route('/product/muscle_gain_results', methods=['GET'])
def muscle_gain_result():
    if current_user.is_anonymous:
        flash('Please sign in to try out services.')
        return redirect(url_for('index'))

    entry = Entry.query.filter_by(user_id=current_user.id).order_by(Entry.created.desc()).first()

    binary_image_string = bytes(entry.image)
    base64_image_string = base64.b64encode(binary_image_string).decode('utf-8')

    context = {'image': base64_image_string,
               'user': current_user.username}

    return render_template('muscle_gain_result.html', context=context)







