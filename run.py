from flask import Flask, render_template, flash, redirect, url_for
from flask_bootstrap import Bootstrap
import front
import sys
import os
import logging

cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None

app = Flask(__name__)
app.config.from_object(front.Config)
bootstrap = Bootstrap(app)
testing = False

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route('/')
@app.route('/index')
def index():
	global testing
	if testing:
		testing = False
		return redirect(url_for('display_stats'))
	return redirect(url_for('find_restaurants'))

@app.route('/display_restaurants')
def display_stats():
    return render_template('display_template.html', rest=front.rest,\
    top_review=front.top_review, ad_rests=front.ad_rests, photos=front.photos)

@app.route('/find_restaurants', methods=['GET', 'POST'])
def find_restaurants():
    form = front.SearchForm()
    if form.validate_on_submit():
        front.submit(form.city.data, form.cuisine.data, form.day.data,\
		[form.time.data.hour, form.time.data.minute])
        return redirect(url_for('display_stats'))
    return render_template('search_template.html', form=form)

if __name__ == '__main__':
	if len(sys.argv) > 1 and sys.argv[1].isnumeric():
		test_case_n = int(sys.argv[1])
		front.test_case(test_case_n)
		testing = True
	os.system('xdg-open http://127.0.0.1:5000/')
	app.run(debug=False)
	

