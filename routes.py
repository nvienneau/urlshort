from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash, _app_ctx_stack
from dbmodel import db, URL
from form import ShortenForm
from shortner import shortenURL

import os, time, json, datetime


#Setting up the Database and Flask App
app = Flask(__name__)

SECRET_KEY = 'development key'
DEBUG = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'urls.db')

app.config.from_object(__name__)
app.config.from_envvar('CHAT_SETTINGS', silent=True)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


#This really doesn't make the url shorter, could modify host file to redirect to something like surl
#but for demo purposes this is fine and is easy to remedy in production env
BASE_DOMAIN = '127.0.0.1:5000'


#Command to create database
@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    db.create_all()


#Handle Logic pertaining to generating a shortened url
@app.route('/', methods=('GET', 'POST'))
def homepage():
	
	form = ShortenForm()
	
	if form.validate_on_submit():
		
		#Do a redundancy check make sure url has not already been used in db
		rdcheck = URL.query.filter_by(url=form.site.data).first()
		
		if rdcheck is not None:
			#No need for user to know the url is already in the db, just render template normally
			surl = rdcheck.surl
		else:
			
			response = redirect(form.site.data)
			print(response.status)
			
			surl = shortenURL()
			db.session.add(URL(surl=surl, url=form.site.data))
			db.session.commit()
		
		return render_template("url.html", url=BASE_DOMAIN + "/" + surl)
	else:
		return render_template("homepage.html", form=form)

#Redirect using Base Domain and the shortened url
@app.route("/<surl>")	
def redirectTo(surl):
	
	dbq = URL.query.filter_by(surl=surl).first()
	db.session.commit()
		
	return redirect(dbq.url)

if __name__ == 'main':
    app.run(debug=True)