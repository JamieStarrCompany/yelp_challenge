from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import SearchForm
import graph 

name = ''
address = ''
rating = 0
review_count = 0

def get_stats(rest_name, rest_address, stars, rest_review_count):
	global name
	global address
	global rating
	global review_count
	
	name = rest_name
	address = rest_address
	rating = stars 
	review_count = rest_review_count

@app.route('/')
@app.route('/index')
def index():
	return render_template('base.html')

@app.route('/display_restaurants')
def display_stats():
	print(name)
	print(address)
	print(rating)
	print(review_count)
	return render_template('display_template.html', name=name, address=address, rating=rating, review_count=review_count)

@app.route('/find_restaurants', methods=['GET', 'POST'])
def find_restaurants():
	form = SearchForm()
	if form.validate_on_submit():
		flash('City to search in {}'.format(form.city.data))
		flash('Cuisine {}'.format(form.cuisine.data))
		flash('Day {}'.format(form.day.data))
		flash('Time {}'.format(form.time.data))

		graph.get_input(form.city.data, form.cuisine.data, form.day.data, form.time.data)
		return redirect(url_for('display_stats'))
		
	return render_template('search_template.html', form=form)


