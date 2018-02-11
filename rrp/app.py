from flask import Flask, session, redirect, render_template, request, \
                  g, flash, url_for, abort
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////rrpdb.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:my-secret-pw@localhost/rrpdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Something not easy to guess'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class TimestampMixin(object):
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

class User(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    salary_number = db.Column(db.String(7))
    name = db.Column(db.String(128))
    password = db.Column(db.String(128))
    email = db.Column(db.String(128))
    role = db.Column(db.String(32))
    enabled_flag = db.Column(db.Boolean)
    requests = db.relationship('Request', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.salary_number

    def is_valid_user(self, password):
        return self.password == password and self.enabled_flag is not None

class Request(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    data_file_full_loc = db.Column(db.String(1024))
    comments = db.Column(db.Text)
    status = db.Column(db.String(32), default='Submitted')

    def __repr__(self):
        return '<Request %r>' % self.data_file_full_loc


class Rule(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    def __repr__(self):
        return '<Rule %r>' % self.name

class Field(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    field_name = db.Column(db.String(32))
    table_name = db.Column(db.String(32))
    scheme_name = db.Column(db.String(32))

    def __repr__(self):
        return '<Field %r>' % self.field_name

request_rule_mapping = db.Table('request_rule_mapping',
    db.Column('request_id', db.Integer, db.ForeignKey('request.id'), primary_key=True),
    db.Column('rule_id', db.Integer, db.ForeignKey('rule.id'), primary_key=True)
)

request_field_mapping = db.Table('request_field_mapping',
    db.Column('request_id', db.Integer, db.ForeignKey('request.id'), primary_key=True),
    db.Column('field_id', db.Integer, db.ForeignKey('field.id'), primary_key=True)
)


""" Start the logic """

@app.route('/')
def show_requests():
    if not session.get('logged_in'):
        error = 'Please login first'
        return render_template('login.html', error=error)
    else:
        fields = Field.query.all()
        rules = Rule.query.order_by('created_at').all()
        requests = Request.query.all()
        curr_user = User.query.get(session['user_id'])
        return render_template('show_requests.html', 
                                requests=requests, 
                                user=curr_user, 
                                fields=fields,
                                rules=rules)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        u = User.query.filter_by(salary_number=request.form['username']).first()
        if not u:
            # Not even a valid salary number in system
            error = 'Salary Number is not found in the system!'
        elif not u.is_valid_user(request.form['password'].strip()):
            error = 'Password is wrong!'
        else:
            session['logged_in'] = True
            session['user_id'] = u.id
            flash('You were logged, welcome {uname}'.format(uname=u.name))
            return redirect(url_for('show_requests'))
    return render_template('login.html', error=error)

@app.route('/add', methods=['POST'])
def add_request():
    if not session.get('logged_in'):
        abort(401)
    flash('New request was successfully posted')
    return redirect(url_for('show_requests'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_requests'))