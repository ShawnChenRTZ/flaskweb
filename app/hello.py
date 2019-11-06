from flask import Flask,render_template,session,redirect,url_for,flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField,PasswordField,BooleanField,SubmitField
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'jhgf34567dsdfkgffd@#$#589g8h876'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/flaskweb?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app,db)
bootstrap = Bootstrap(app)

# 定义模型Role
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    users = db.relationship('User',backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name
# 定义模型User
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500

class NameForm(FlaskForm):
    name = StringField("what's your name?",validators=[DataRequired()])
    submit = SubmitField('submit')

class LoginForm(FlaskForm):
    username = StringField('账号',validators=[DataRequired(message='请输入账号')])
    password = PasswordField('密码',validators=[DataRequired(message='请输入密码')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

@app.route('/',methods=['POST','GET'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        # 比对两次输入的name，不同时给出flash消息
        # old_name = session.get('name')
        # if old_name is not None and old_name != form.name.data:
        #     flash("It's a flash message-Looks like you have changed your name!")
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'),known=session.get('known',False))

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    return render_template('login.html',form=form)


if __name__ =='__main__':
    app.run(debug=True)