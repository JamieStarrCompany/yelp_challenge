from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField#, PasswordField, StringField, BooleanField
from wtforms_components import TimeField

import os

from mid import recommend_rest, get_top_review, recommend_5_rest,\
get_city_list, get_cuisine_list

rest = None
top_review = None
ad_rests = []

class Config(object):
	#In flask (and in its extensions) , we sometimes us the value of the secret key
	#as a crypographic key -> useful to gen signatures or tokens
	#FlaskWTF uses it to protect web forms from CSRF (cross site request forgery) attacks
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'


class SearchForm(FlaskForm):
	city = SelectField(u'City', choices=get_city_list())

	cuisine = SelectField(u'Cuisine', choices=get_cuisine_list())

	day = SelectField(u'Day', choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')])
	time = TimeField('Time')
	search = SubmitField('Search')


def submit(city, cuisine, day, time):
	global rest
	global top_review
	global ad_rests

	rest = recommend_rest(city, cuisine, day, [time.hour, time.minute])
	top_review = get_top_review(rest)
	if rest and top_review:
		ad_rests = recommend_5_rest(top_review['u']['id'],\
		rest['rest']['name'], city, cuisine)
