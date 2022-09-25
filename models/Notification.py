def Notification_(db):

	notifications = db.Table('notifications',
	                   db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
	                   db.Column('friend_id', db.Integer, db.ForeignKey('user.id')))

	return notifications
