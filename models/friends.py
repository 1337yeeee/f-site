def Friends_(db):

	friends = db.Table('friends',
	                   db.Column('user1_id', db.Integer, db.ForeignKey('user.id')),
	                   db.Column('user2_id', db.Integer, db.ForeignKey('user.id')))

	return friends
