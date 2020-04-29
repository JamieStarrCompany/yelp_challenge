import os

class Config(object):
	#In flask (and in its extensions) , we sometimes us the value of the secret key 
	#as a crypographic key -> useful to gen signatures or tokens
	#FlaskWTF uses it to protect web forms from CSRF (cross site request forgery) attacks
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'