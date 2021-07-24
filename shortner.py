import string
from random import choice, randint
from dbmodel import db, URL

#Simple function that generates a 6 digit token to be used
#In a loop for simplicity sake as the chances of a collision occuring are low due to there
#being 62^6+62^5+62^4.... possible combinations.
def shortenURL():
	#Use base62 instead of base64 because '+' and '/' are ugly	
	base62 = string.digits + string.ascii_letters
	
	in_use = True
	while in_use:
		surl = "".join(choice(base62) for i in range(randint(1,6)))
		if not db.session.query(db.session.query(URL).filter_by(surl=surl).exists()).scalar():
			in_use = False
			break
	
	return surl
