def User_(db, friends_, notifications_):

	class User(db.Model):
		id = db.Column(db.Integer, primary_key=True)
		login = db.Column(db.String(20), nullable=False, unique=True)
		password = db.Column(db.String(20), nullable=False)
		name = db.Column(db.String(20), nullable=False)
		description = db.Column(db.String(160), default='No description')
		friends = db.relationship(
			'User', secondary=friends_,
			primaryjoin=(friends_.c.user1_id == id),
			secondaryjoin=(friends_.c.user2_id == id),
			backref=db.backref('friends_', lazy='dynamic'), lazy='dynamic')
		notifications = db.relationship(
			'User', secondary=notifications_,
			primaryjoin=(notifications_.c.user_id == id),
			secondaryjoin=(notifications_.c.friend_id == id),
			backref=db.backref('notifications_', lazy='dynamic'), lazy='dynamic')

		def __repr__(self):
			return '<User %r>' % self.login

		def is_friend(self, user):
			return self.friends.filter(
				friends_.c.user2_id == user.id).count() > 0

		def unfriend(self, user):
			if self.is_friend(user):
				self.friends.remove(user)
				try:
					db.session.commit()
				except:
					pass

		def dofriend(self, user):
			if not self.is_friend(user):
				self.delete_notification(user)
				self.friends.append(user)
				if not user.is_friend(self):
					user.friends.append(self)
				try:
					db.session.commit()
				except:
					pass

		def add_notification(self, user):
			if self.is_friend(user):
				pass
			elif not self.is_in_notifications(user):
				self.notifications.append(user)
				try:
					db.session.commit()
				except:
					pass

		def is_notification(self):
			return self.notifications.filter(
				notifications_.c.user_id == self.id).count() > 0

		def get_notifications(self):
			return self.notifications.filter(notifications_.c.user_id == self.id).all()

		def delete_notification(self, user):
			if self.is_notification():
				self.notifications.remove(user)
			try:
				db.session.commit()
			except:
				pass

		def is_in_notifications(self, user):
			return user in self.get_notifications()

	return User
