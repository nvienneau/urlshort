import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#URL Data Model
#url is original url
#surl is shortened url
#uses is number of times surl has been used
class URL(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	url = db.Column(db.String(1600),index=True, unique=True, nullable=False)
	surl = db.Column(db.String(32), index=True, unique=True, nullable=False)
	uses = db.Column(db.Integer, nullable=False, default=0)
	created = db.Column(db.DateTime, default=datetime.datetime.now)
	
	def __repr__(self):
		return "'{self.id}' '{self.url}' '{self.surl}' '{self.uses}'"
