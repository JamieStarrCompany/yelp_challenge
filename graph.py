import requests
from jinja2 import Template
from flask import Flask
from py2neo import Graph
import passw
import re
import run

#--------------------------------------------------------------------------------#
#	GLOBAL VARIABLES
#--------------------------------------------------------------------------------#

city = ''
cuisine = ''
day = ''
time = ''

graph = ''

#--------------------------------------------------------------------------------#
#	GRAPH CODE
#--------------------------------------------------------------------------------#

#Only to be run once in it's lifetime
def init_graph():
	your_password = passw.ord()
	uri = "bolt://neo4j:{}@localhost:8000".format(your_password)
	global graph
	graph = Graph(uri)

	#Clean graph
	graph.evaluate("MATCH (n) DETACH DELETE n")

	#Set up key\val with APOC schema.assert
	graph.evaluate("CALL apoc.schema.assert({Category:['name']},{Business:['id'],User:['id'],Review:['id']})")

	#Load business.json, user.json and review.json respectivelu
	graph.evaluate('CALL apoc.periodic.iterate("'
               'CALL apoc.load.json(\'file:///business.json\') YIELD value RETURN value '
               '"," '
               'MERGE (b:Business{id:value.business_id}) '
               'SET b += apoc.map.clean(value, [\'business_id\',\'categories\',\'address\',\'postal_code\'],[]) '
               'WITH b,value.categories as categories '
               'UNWIND categories as category '
               'MERGE (c:Category{id:category}) '
               'MERGE (b)-[:IN_CATEGORY]->(c)"'
               ',{batchSize: 10000, iterateList: true});')

	graph.evaluate('CALL apoc.periodic.iterate("'
               'CALL apoc.load.json(\'file:///user.json\') '
               'YIELD value RETURN value '
               '"," '
               'MERGE (u:User{id:value.user_id}) '
               'SET u += apoc.map.clean(value, [\'friends\',\'user_id\'],[0]) '
               'WITH u,value.friends as friends '
               'UNWIND friends as friend '
               'MERGE (u1:User{id:friend}) '
               'MERGE (u)-[:FRIEND]-(u1) '
               '",{batchSize: 100, iterateList: true});')
	
	graph.evaluate('CALL apoc.periodic.iterate("'
               'CALL apoc.load.json(\'file:///review.json\') '
               'YIELD value RETURN value '
               '"," '
               'MERGE (b:Business{id:value.business_id}) '
               'MERGE (u:User{id:value.user_id}) '
               'MERGE (u)-[r:REVIEWS]->(b) '
               'SET r += apoc.map.clean(value, [\'business_id\',\'user_id\',\'review_id\'],[0])'
               '",{batchSize: 10000, iterateList: true});')

def open_graph():
        
	uri = "bolt://neo4j:{0}@localhost:8000".format(passw.ord())
	global graph
	graph = Graph(uri)
	

#--------------------------------------------------------------------------------#
# 	CHRISTIAAN & LAUREN
#--------------------------------------------------------------------------------#

def fetch(city, cuisine, day, time):
	#time format: 00:00-00:00
	#All data must be in CamelCase
	time = time.split('-')
	day = day.lower()
	cypher = "MATCH (rest:Business)-[:IN_CATEGORY]->(Category {id: '%s'}) WHERE rest.city='%s' RETURN rest"%(cuisine, city)
	return graph.run(cypher).data()		#RETURNS list of dictionaries

def get_reviews(restaurant): #dict object
	id = restaurant['id']
	cypher = "MATCH (:Business {id : '%s'})<-[r:REVIEWS]-(u:User) RETURN r, u"%(id)
	return graph.run(cypher).data()

def get_social_circle(user):
	id = user['id']
	cypher = "MATCH (u:User {id : '%s'})-[:FRIEND*1..2]-(b:User)-[r:REVIEWS]-(:Business) RETURN b, COUNT(r) ORDER BY COUNT(r) DESC LIMIT 50"%(id)
	return graph.run(cypher).data()

#sorts and finds which restaurant to recommend
def get_reviews_by_50(users, city, cuisine): #users are list of dict, other are strings
	full_list = list()
	for user in users:
		id = user['b'].get('id')
		cypher = "MATCH (:User {id : '%s'})-[r:REVIEWS]->(b:Business)-[:IN_CATEGORY]->(Category {id: '%s'}) WHERE b.city = '%s' RETURN r"%(id, cuisine, city)
		temp_list = graph.run(cypher).data()
		full_list = full_list + temp_list

	return full_list

def get_images(bussiness):
	id = bussiness['id']
	
#--------------------------------------------------------------------------------#
#	ADAM & JOHAN
#--------------------------------------------------------------------------------#


# !NEEDS FIXING! #
#Sort by stars, tie break by review count
def recommend_rest(restaurants): #restaurants is list of dictionaries
	#sorted_list  = sorted(restaurants, reverse= True, key= lambda k: (k['stars'],k['review_count']))
	sorted_list  = sorted(restaurants, reverse= True, key= lambda k: ('stars','review_count'))
	return sorted_list[0]['rest']

# !NEEDS FIXING! #
def get_top_review(reviews): #list of dictionaries
	#sorted_list = sorted(reviews, reverse= True, key= lambda k: (k['useful']) )
	sorted_list = sorted(reviews, reverse= True, key= lambda k: ('useful'))	
	return sorted_list[0]

#sort by highest review count
#NOT NEEDED ANYMORE
def get_50_reviewers(users):
	sorted_reviews = sorted(reviews, reverse=True, key=lambda x: (x['review_count']))
	if len(sorted_reviews) < 50:
		return sorted_reviews
	return sorted_reviews[:50]


def filter_reviews(reviews):
	if len(reviews) == 0:
		return reviews
	

#--------------------------------------------------------------------------------#
#	SARAH
#--------------------------------------------------------------------------------#

def get_input(form_city, form_cuisine, form_day, form_time):
	global city
	global cuisine
	global day
	global time
	
	city = form_city
	cuisine = form_cuisine
	day = form_day
	time = form_time

#information all within the dict object
def display_stats(restaurant, reviews):
	name = restaurant['rest'].get('name')
	address = restaurant['rest'].get('address')
	stars = restaurant['rest'].get('stars')
	review_count = len(reviews)

	print('---------------------------')
	print('Top Restaurant:')
	print('---------------------------')
	print(name)
	print(address)
	print("Rating: " + stars)
	print('Number of reviews: ' + str(review_count))
	print('---------------------------')



def display_useful_review(review): 
	text = review['r'].get('text')
	username = review['u'].get('name')
	stars = review['r'].get('stars')
	#stars
	print('Top Review:')
	print('---------------------------')
	print('Name: ' + username)
	print('Stars: ' + str(stars))
	print()
	print(text)
	print()
	print('---------------------------')



def display_photos(restaurant):
	print(' -------------')
	print('|             |')
	print('|             |')
	print('|    piktur   |')
	print('|             |')
	print('|             |')
	print(' -------------')
	print()

def display_recommendation(top_5_restaurants):
	print("Other restaurants enjoyed by people like you:")
	print('---------------------------')
	print()
	if len(top_5_restaurants) == 0:
		print('Whoops!')
		print("Our sources have come up empty...")
	else:
		for restaurant in top_5_restaurants:
			display_stats(restaurant)
	
	print('---------------------------')


#--------------------------------------------------------------------------------#
#	RUN
#--------------------------------------------------------------------------------#
def main():
	open_graph()

	#--------------------------------------------------------------------------------#
	#Part 1: Recommend a restaurant with it's review
	#--------------------------------------------------------------------------------#
	get_input()

	#TEST CODE#
	city = 'Mesa'
	cuisine = 'Cafes'
	day = 'Wednesday'
	time = '09:00-11:00'
	##

	rest_results = fetch(city, cuisine, day, time) #rest_results is a list of dicts
	restaurant = run.recommend_rest(rest_results) #restaurant should be a dict object
	reviews_result = get_reviews(restaurant['rest']) #list of dictionaries, including the reviews and their users
	top_review = run.get_top_review(reviews_result) #dict object
	print(top_review)

	#--------------------------------------------------------------------------------#
	# Part 2: Recommend 5 more restaurants based on 50 other users
	#--------------------------------------------------------------------------------#
	circle = get_social_circle(dict(top_review.get('u'))) #circle is list of dicts of max len 50
	reviews_by_50 = get_reviews_by_50(circle, city, cuisine) #list of dict
	top_5_restaurants = filter_reviews(reviews_by_50) #list of dict
	
	#--------------------------------------------------------------------------------#
	#Part 3: Display information
	#--------------------------------------------------------------------------------#
	display_stats(restaurant, reviews_result)
	display_useful_review(top_review)
	display_photos(restaurant)
	display_recommendation(top_5_restaurants)

if __name__ == '__main__':
	main()
