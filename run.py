from flask import Flask, render_template, flash, redirect, url_for
import front


app = Flask(__name__)
app.config.from_object(front.Config)

@app.route('/')
@app.route('/index')
def index():
	return render_template('base.html')

@app.route('/display_restaurants')
def display_stats():
    name = front.rest['rest']['name']
    address = ""
    rating = 5
    review_count = 0
    return render_template('display_template.html', name=name, address=address, rating=rating, review_count=review_count)


@app.route('/find_restaurants', methods=['GET', 'POST'])
def find_restaurants():
    form = front.SearchForm()
    if form.validate_on_submit():
        flash('City to search in {}'.format(form.city.data))
        flash('Cuisine {}'.format(form.cuisine.data))
        flash('Day {}'.format(form.day.data))
        flash('Time {}'.format(form.time.data))

        front.submit(form.city.data, form.cuisine.data, form.day.data, form.time.data)
        return redirect(url_for('display_stats'))
    return render_template('search_template.html', form=form)

if __name__ == '__main__':
	app.run(debug=True)
