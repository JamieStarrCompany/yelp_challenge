from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms_components import TimeField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
	city = SelectField(u'City', choices=[('Phoenix', 'Phoenix'),('Cave Creek', 'Cave Creek'), ('Surprise', 'Surprise'),('Scottsdale', 'Scottsdale'),('Chandler', 'Chandler'), ('Fountain Hills', 'Fountain Hills'), ('Peoria', 'Peoria'),('Glendale', 'Glendale'), ('Goodyear', 'Goodyear'), ('Tempe', 'Tempe'),('Avondale', 'Avondale'), ('Mesa', 'Mesa'), ('Gilbert', 'Gilbert')])
	
	cuisine = SelectField(u'Cuisine', choices=[('African', 'African'),('American (New)', 'American (New)'),('American (Traditional)','American (Traditional)'),('Asian Fusion', 'Asian Fusion'),('Barbeque', 'Barbeque'),('Breakfast & Brunch', 'Breakfast & Brunch'),('Buffets','Buffets'),('Burgers','Burgers'),('Cafes','Cafes'),('Caribbean','Caribbean'),('Chicken Wings','Chicken Wings'),('Chinese', 'Chinese'),('Comfort Food', 'Comfort Food'),('Delis', 'Delis'),('Diners', 'Diners'),('Fast Food', 'Fast Food'),('French', 'French'),('Gluten-Free', 'Gluten-Free'),
	('Greek', 'Greek'),('Indian', 'Indian'),('Italian', 'Italian'),('Kebab', 'Kebab'),('Korean', 'Korean'),('Latin American', 'Latin American'),('Mediterranean', 'Mediterranean'),('Mexican', 'Mexican'),('Middle Eastern', 'Middle Eastern'),('Noodles', 'Noodles'),
	('Pizza', 'Pizza'),('Salad', 'Salad'),('Sandwiches', 'Sandwiches'),('Seafood','Seafood'),('Soup','Soup'),('Southern', 'Southern'),('Spanish', 'Spanish'),
	('Steakhouses', 'Steakhouses'),('Sushi Bars', 'Sushi Bars'),('Tacos', 'Tacos'),('Tex-Mex', 'Tex-Mex'),('Vegan', 'Vegan'),('Vegetarian', 'Vegetarian'),('Vietnamese', 'Vietnamese')])
	
	day = SelectField(u'Day', choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')])
	time = TimeField('Time')
	search = SubmitField('Search')
