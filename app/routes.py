from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import SearchForm
import graph 

@app.route('/')
@app.route('/index')
def index():
	
	return render_template('base.html')

@app.route('/find_restaurants', methods=['GET', 'POST'])
def find_restaurants():
	form = SearchForm()
	if form.validate_on_submit():
		flash('City to search in {}'.format(form.city.data))
		flash('Cuisine {}'.format(form.cuisine.data))
		flash('Day {}'.format(form.day.data))
		flash('Time {}'.format(form.time.data))

		graph.get_input(form.city.data, form.cuisine.data, form.day.data, form.time.data)
		# return redirect(url_for('index'))
		
	return render_template('search_template.html', form=form)
