from flask import Flask, session, redirect, render_template, request, \
                  g, flash, url_for, abort
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from werkzeug.security import generate_password_hash, \
     check_password_hash

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

request_rule_mapping = db.Table('request_rule_mapping',
    db.Column('request_id', db.Integer, db.ForeignKey('request.id'), primary_key=True),
    db.Column('rule_id', db.Integer, db.ForeignKey('rule.id'), primary_key=True)
)

request_field_mapping = db.Table('request_field_mapping',
    db.Column('request_id', db.Integer, db.ForeignKey('request.id'), primary_key=True),
    db.Column('field_id', db.Integer, db.ForeignKey('field.id'), primary_key=True)
)

class User(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    salary_number = db.Column(db.String(7))
    name = db.Column(db.String(128))
    hs_password = db.Column(db.String(128))
    email = db.Column(db.String(128))
    role = db.Column(db.String(32))
    enabled_flag = db.Column(db.Boolean)
    requests = db.relationship('Request', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.salary_number

    @property
    def password(self):
        return self.hs_password
    
    @password.setter
    def password(self, v):
        self.hs_password = generate_password_hash(v)


    def is_valid_user(self, password):
        return check_password_hash(self.hs_password, password) and self.enabled_flag is not None

class Request(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    data_file_full_loc = db.Column(db.String(1024))
    comments = db.Column(db.Text)
    status = db.Column(db.String(32), default='Submitted')

    fields = db.relationship("Field", secondary=request_field_mapping)
    rules = db.relationship("Rule", secondary=request_rule_mapping)


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



""" Start the logic """
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/help')
def show_help():
    return render_template('help.html')

@app.route('/r/<request_id>')
def show_request_detail(request_id):
    if not session.get('logged_in'):
        error = 'Please login first'
        return render_template('login.html', error=error)
    curr_user = User.query.get(session['user_id'])
    r = Request.query.get_or_404(request_id)
    if r.user_id == curr_user.id:
        return render_template('show_request_detail.html', request=r)
    else:
        abort(404)

@app.route('/')
def show_requests():
    if not session.get('logged_in'):
        error = 'Please login first'
        return render_template('login.html', error=error)
    else:
        fields = Field.query.all()
        rules = Rule.query.order_by('created_at').all()
        requests = sorted(Request.query.all(),key=lambda x:x.created_at, reverse=True)
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

@app.route('/del/<request_id>')
def del_request(request_id):
    if not session.get('logged_in'):
        error = 'Please login first'
        return render_template('login.html', error=error)
    curr_user = User.query.get(session['user_id'])
    r = Request.query.get_or_404(request_id)
    if r.user_id == curr_user.id:
        db.session.delete(r)
        db.session.commit()
        flash('Request has been deleted')
        return redirect(url_for('show_requests'))
    else:
        abort(404)

@app.route('/add', methods=['POST'])
def add_request():
    if not session.get('logged_in'):
        abort(401)
    curr_user = User.query.get(session['user_id'])
    req = Request(
        user_id = curr_user.id,
        data_file_full_loc = request.form['file_loc'],
        comments = request.form['comments']
    )
    for rule_id in request.form.getlist('ruleslist[]'):
        print('Debug: rule id {}'.format(rule_id))
        req.rules.append(Rule.query.get(rule_id))

    for field_id in request.form.getlist('fieldslist[]'):
        req.fields.append(Field.query.get(field_id))
    
    db.session.add(req)
    db.session.commit()

    flash('New request was successfully posted')
    return redirect(url_for('show_requests'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_requests'))