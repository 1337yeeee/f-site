from __init__ import *
from models import user


@app.route('/')
def index():
	active_user_id = request.cookies.get('active_user')
	if active_user_id is not None:
		active_user = User.query.filter_by(id=active_user_id).first()
		return render_template('index.html', user=active_user, is_notification=active_user.is_notification())
	else:
		return render_template('index.html', user=None, is_notification=False)


@app.route('/sign_in', methods=['POST', 'GET'])
def sign_in():
	if request.method == 'POST':
		try:
			user = User.query.filter_by(login=request.form['login'],
			                            password=request.form['password']).first()
			if user:
				resp = make_response(redirect('/'))
				resp.set_cookie('active_user', str(user.id))
				return resp
			else:
				return 'Wrong login and/or password'
		except:
			return 'There is an issue searching user in db\n\t\tsign_in()'
	else:
		return render_template('sign_in.html')


@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
	if request.method == 'POST':
		new_user = User(login=request.form['login'],
		                name=request.form['name'],
		                password=request.form['password'])

		try:
			db.session.add(new_user)
			db.session.commit()
			resp = make_response(redirect('/'))
			resp.set_cookie('active_user', str(new_user.id))
			return resp
		except:
			return 'There is an issue with adding a new user into db at \n\t\tsign_up()'
	else:
		return render_template('sign_up.html')


@app.route('/sign_out')
def sign_out():
	resp = make_response(redirect('/'))
	resp.delete_cookie('active_user')
	return resp


@app.route('/my_page')
def my_page():
	active_user_id = request.cookies.get('active_user')
	active_user = User.query.filter_by(id=active_user_id).first()
	return render_template('my_page.html', user=active_user, is_notification=active_user.is_notification())


@app.route('/my_page/change_desc', methods=['POST', 'GET'])
def change_desc():
	if request.method == 'POST':
		new_description = request.form['description']
		active_user_id = request.cookies.get('active_user')
		active_user = User.query.filter_by(id=active_user_id).first()
		active_user.description = new_description
		try:
			db.session.commit()
			return redirect('/my_page')
		except:
			return 'There is an issue with updating the description\n\t\t!change_desc()'
	else:
		active_user_id = request.cookies.get('active_user')
		active_user = User.query.filter_by(id=active_user_id).first()
		return render_template('change_desc.html', user=active_user, is_notification=active_user.is_notification())


@app.route('/search')
def search():
	search_text = request.args.get('search_text')
	users = User.query.filter(User.name.contains(search_text)).all()
	return render_template('search.html', users=users)


@app.route('/user/<user_id>')
def user_(user_id):
	user = User.query.filter_by(id=user_id).first()
	if user_id == request.cookies.get('active_user'):
		return redirect('/my_page')
	elif user:
		active_user = user.query.filter_by(id=request.cookies.get('active_user')).first()
		if user.is_friend(active_user):
			return render_template('user.html', user=user, is_friend=True,
			                       is_notification=active_user.is_notification())
		elif active_user.is_in_notifications(user):
			return render_template('user.html', user=user, is_friend=False, is_request=True,
			                       is_notification=active_user.is_notification())
		elif user.is_in_notifications(active_user):
			return render_template('user.html', user=user, is_friend=False, sent_request=True,
			                       is_notification=active_user.is_notification())
		else:
			return render_template('user.html', user=user, is_friend=False,
			                       is_notification=active_user.is_notification())
	else:
		return render_template('NotFound.html')


@app.route('/user/<user_id>/add_friend')
def user_add_friend(user_id):
	active_user_id = request.cookies.get('active_user')
	active_user = User.query.filter_by(id=active_user_id).first()
	user = User.query.filter_by(id=user_id).first()
	user.add_notification(active_user)

	return redirect(f'/user/{user_id}')


@app.route('/user/<user_id>/cancel_request')
def user_cancel_request(user_id):
	active_user_id = request.cookies.get('active_user')
	active_user = User.query.filter_by(id=active_user_id).first()
	user = User.query.filter_by(id=user_id).first()
	user.delete_notification(active_user)

	return redirect(f'/user/{user_id}')


@app.route('/user/<user_id>/accept')
def user_accept(user_id):
	active_user_id = request.cookies.get('active_user')
	active_user = User.query.filter_by(id=active_user_id).first()
	user = User.query.filter_by(id=user_id).first()
	active_user.dofriend(user)

	return redirect(f'/user/{user_id}')


@app.route('/user/<user_id>/del_friend')
def user_del_friend(user_id):
	active_user_id = request.cookies.get('active_user')
	active_user = User.query.filter_by(id=active_user_id).first()
	user = User.query.filter_by(id=user_id).first()
	active_user.unfriend(user)
	user.unfriend(active_user)

	return redirect(f'/user/{user_id}')


@app.route('/notifications')
def notify():
	active_user_id = request.cookies.get('active_user')
	active_user = User.query.filter_by(id=active_user_id).first()
	users_notifications = active_user.get_notifications()
	return render_template('notifications.html', user=active_user, is_notification=(len(users_notifications) > 0),
	                       notifications=users_notifications)


@app.route('/accept/<int:friend_id>')
def accept(friend_id):
	active_user_id = request.cookies.get('active_user')
	active_user = User.query.filter_by(id=active_user_id).first()
	friend = User.query.filter_by(id=friend_id).first()
	active_user.dofriend(friend)
	return redirect(f'/user/{friend_id}')


if __name__ == '__main__':
	app.run(debug=True)
	# user = User.query.filter_by(id=1).first()
	# user.get_notifications()
