from app import app #从app包中导入 app这个实例
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm
from app.models import User
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm

#路由
@app.route('/')
@app.route('/index')
@login_required
#1个视图函数
def index():
	#user = {'username':'Miguel'}
	posts = [#创建一个列表：帖子。里面元素是两个字典，每个字典里元素还是字典，分别作者、帖子内容。
		{
			'author': {'username':'John'},
			'body':'Beautiful day in Portland!'
		},
		{
			'author': {'username':'Susan'},
			'body':'The Avengers movie was so cool!'
		}
	]
	#return render_template('index.html', title='Home', user=user, posts=posts)
	return render_template('index.html', title='Home', posts=posts)

@app.route('/login',methods=['GET','POST'])
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
		#flash('Login requested for user {},remember_me={}'.format(form.username.data,form.remember_me.data))
		# 重定向到 next 页面
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
		#return redirect(url_for('index'))
	return render_template('login.html',title='Sign In',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods = ['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are now a registered user!')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)
