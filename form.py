import socket
from urllib.parse import urlparse
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Optional
from dbmodel import db, URL

#As a further precaution, do not store or deal with any urls with length less than 6
#Frees up more tokens
def checkURL(form, field):

	dname = urlparse(field.data)
	print(dname.netloc)
	#Don't bother storing urls that do not exist
	try:
		socket.gethostbyname(dname.netloc)
	except socket.gaierror:
		raise ValidationError("No DNS Entry exists for inputted url")
	

	#As a further precaution, do not store or deal with any urls with length less than 6
	#Frees up more tokens
	if len(field.data) < 6 or len(field.data) > 1600:
		raise ValidationError("URLS must be at least 6 characters long")
	
	if len(field.data) > 1600:
		raise ValidationError("URLS Must be less than 1600 characters")
	
	if (" " in field.data):
		raise ValidationError("Invalid URL: Input contains spaces")
	
	if not("." in field.data):
		raise ValidationError("Invalid URL: Input has no domain name i.e .com")

	if field.data.count(".") > 1:
		raise ValidationError("Invalid URL: URL Can only have one domain name i.e .com")
	
	if not(field.data.lower().startswith("http://")) and not(field.data.lower().startswith("https://")):
		field.data = "http://" + field.data
	
	

class ShortenForm(FlaskForm):

	site = StringField(validators=[DataRequired(), Length(min=6, max=1600, message="Invalid Length"), checkURL])
	shorten = SubmitField("Shorten")