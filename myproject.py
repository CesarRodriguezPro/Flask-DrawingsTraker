
from myprojectLogin import app, db
from flask import render_template, redirect, request, url_for, flash, send_file
from flask_login import login_user, login_required, logout_user
from myprojectLogin.models import User
from myprojectLogin.forms import LoginForm, RegistrationForm, AddForm, DelForm
from datetime import datetime
from myprojectLogin.QRCodeGenerator import create_barcode
import os

''' This is a application to track drawings for IBK construction group.'''

version = "2.1 Creating datepicker"

class DrawingsInfo(db.Model):

    ''' this is for saving the basic information of the drawings to be save inside the database.'''

    __tablename__ = 'Drawings'
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.Text)
    Draw_code = db.Column(db.Text)
    description = db.Column(db.Text)
    date_release = db.Column(db.Text)

    def __init__(self, id, location, Draw_code, description, date_release):
        self.id = id
        self.location = location
        self.Draw_code = Draw_code
        self.description = description
        self.date_release = date_release

    def __repr__(self):
        return '{} - {} -- [ {} ] -- [ {} ] - {}'.format(self.id,self.date_release,  self.location, self.Draw_code, self.description)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/Welcome')
@login_required
def welcome_user():
    return render_template('home.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('you logged out!')
    return redirect(url_for('home'))


@app.route('/login', methods = ['GET', 'POST'])
def login():
    try:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()

            if user.check_password(form.password.data) and user is not None:
                login_user(user)
                flash('Logged in Successfully!')

                next = request.args.get('next')
                if next == None or not next[0] == '/':
                    next = url_for('welcome_user')
                return redirect(next)

        return render_template('login.html', form = form)
    except:
        return render_template('login.html', form = form)


@app.route('/register', methods = ['GET', 'POST'])
@login_required
def register():
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data,
                    username = form.username.data,
                    password = form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash('Thank you for your registeration')
            return redirect(url_for('login'))
        except:
            return render_template('errors.html', warning='That user already exits')

    return render_template('register.html', form = form)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_data():

    form = AddForm()
    if form.validate_on_submit():

        ID = form.ID.data
        location = form.location.data
        drawcode = form.drawcode.data
        description = form.description.data
        summit_date = form.draw_date.data
       
        if DrawingsInfo.query.get(ID):
            dbinfo = DrawingsInfo.query.get(ID)
            dbinfo.location = location
            dbinfo.Draw_code = drawcode
            dbinfo.description = description
            dbinfo.date_release = summit_date.strftime('%Y-%m-%d')

            db.session.add(dbinfo)
            db.session.commit()
            create_barcode(id_number=ID, update_date = summit_date.strftime('%m%d%y'))
           
        else:
            print(summit_date)
            new_item = DrawingsInfo(ID, location, drawcode, description, summit_date.strftime('%Y-%m-%d') )
            db.session.add(new_item)
            db.session.commit()
            create_barcode(id_number=ID, update_date=summit_date.strftime('%m%d%y'))
        
        server_time = datetime.timestamp(datetime.now())
        barcode_url = (f"/static/{ID}.jpg?{server_time}")
        return render_template('add.html', form=form, barcode_url=barcode_url)

    return render_template('add.html', form=form)


@app.route('/list',  methods=['GET', 'POST'])
@login_required
def list_data():

    show_data = DrawingsInfo.query.all()
    if request.method == 'POST':
        search = request.form.get('search')
        if f'{search}.jpg' in os.listdir(os.path.abspath('myprojectLogin/static')):
            server_time = datetime.timestamp(datetime.now())
            barcode_url = (f"/static/{search}.jpg?{server_time}")
            return render_template('list.html', show_data=show_data, barcode_url=barcode_url)
    return render_template('list.html', show_data=show_data)


@app.route('/delete', methods=['GET', 'POST'])
@login_required
def del_data():
    form = DelForm()
    if form.validate_on_submit():
        id = form.id.data
        try:
            del_draw = DrawingsInfo.query.get(id)
            db.session.delete(del_draw)
            db.session.commit()
            return redirect(url_for('list_data'))
        except:
            return render_template('Errors.html', warning = 'That code is not in the Database ')
    return render_template('delete.html', form = form)


@app.route('/ret/<item>')
def check_drawings(item):
    date_in_drawing = item[-6:]
    codeID = item[3:-6]
    try:
        if item[:3] == "xcd":
            data = DrawingsInfo.query.get(codeID)
            code = data.id
            location = data.location
            drawcode = data.Draw_code
            description = data.description
            date_release = data.date_release
            year_d = int('20{}'.format(date_in_drawing[-2:]))
            month_d = int(date_in_drawing[0:2])
            day_d = int(date_in_drawing[2:-2])

            if data:
                if datetime(year = year_d, month = month_d, day = day_d) >= datetime.strptime(data.date_release, '%Y-%m-%d'):
                    return render_template('current.html', code=code, location = location, drawcode= drawcode,
                                           description= description, date_release=date_release)
                else:
                    return render_template('old.html', code=code, location = location, drawcode= drawcode,
                                           description= description, date_release=date_release)
            else:
                return '<h1> Not Found </h1>'
    except:
        return render_template('Errors.html', warning='That Code is Invalid')
    else:
        return render_template('login.html', form = form)


if __name__ == '__main__':
    app.run(debug = True)
    # app.run(host='0.0.0.0')


