from datetime import datetime
from analyzer import db


class Tweet(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), nullable=False)
	user_avatar = db.Column(db.String(200), nullable=False)
	tweet_content = db.Column(db.Text, nullable=False)
	date_posted = db.Column(db.String(50), nullable=False)
	is_technical = db.Column(db.Boolean, nullable=True)

	def __repr__(self):
		return f"<User: {self.username}>, <Content: {self.tweet_content}>, <Age: {self.date_posted}>, <Technical?: {self.is_technical}>"

