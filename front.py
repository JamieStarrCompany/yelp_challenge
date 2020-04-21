from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms_components import TimeField

import os

from mid import recommend_rest, get_top_review, recommend_5_rest,\
get_city_list, get_cuisine_list, get_random_photos
import tests

rest = None
top_review = None
ad_rests = []
photos = []

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'


class SearchForm(FlaskForm):
	city = SelectField(u'City', choices=get_city_list())

	cuisine = cuisine = SelectField(u'Cuisine', choices=[('African', 'African'),('American (New)', 'American (New)'),('American (Traditional)','American (Traditional)'),('Asian Fusion', 'Asian Fusion'),('Barbeque', 'Barbeque'),('Breakfast & Brunch', 'Breakfast & Brunch'),('Buffets','Buffets'),('Burgers','Burgers'),('Cafes','Cafes'),('Caribbean','Caribbean'),('Chicken Wings','Chicken Wings'),('Chinese', 'Chinese'),('Comfort Food', 'Comfort Food'),('Delis', 'Delis'),('Diners', 'Diners'),('Fast Food', 'Fast Food'),('French', 'French'),('Gluten-Free', 'Gluten-Free'),
	('Greek', 'Greek'),('Indian', 'Indian'),('Italian', 'Italian'),('Kebab', 'Kebab'),('Korean', 'Korean'),('Latin American', 'Latin American'),('Mediterranean', 'Mediterranean'),('Mexican', 'Mexican'),('Middle Eastern', 'Middle Eastern'),('Noodles', 'Noodles'),
	('Pizza', 'Pizza'),('Salad', 'Salad'),('Sandwiches', 'Sandwiches'),('Seafood','Seafood'),('Soup','Soup'),('Southern', 'Southern'),('Spanish', 'Spanish'),
	('Steakhouses', 'Steakhouses'),('Sushi Bars', 'Sushi Bars'),('Tacos', 'Tacos'),('Tex-Mex', 'Tex-Mex'),('Vegan', 'Vegan'),('Vegetarian', 'Vegetarian'),('Vietnamese', 'Vietnamese')])

	day = SelectField(u'Day', choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')])
	time = TimeField('Time', format='%H:%M')
	search = SubmitField('Search')


def submit(city, cuisine, day, time):
	global rest
	global top_review
	global ad_rests
	global photos

	rest = recommend_rest(city, cuisine, day, time)
	photos = get_random_photos(rest, 3)
	top_review = get_top_review(rest)
	if rest and top_review:
		ad_rests = recommend_5_rest(top_review['u']['id'],\
		rest['rest']['name'], city, cuisine)

def test_case(n):
	s = tests.get_scenario(n)
	if s:
		submit(s[0], s[1], s[2], s[3])
