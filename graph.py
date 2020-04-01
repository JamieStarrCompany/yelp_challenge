from jinja2 import Template
from flask import Flask
from py2neo import Graph

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
	your_password = 'asshat1234'
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
	uri = "bolt://neo4j:asshat1234@localhost:8000"
	global graph
	graph = Graph(uri)
	

#--------------------------------------------------------------------------------#
# 	CHRISTIAAN & LAUREN
#--------------------------------------------------------------------------------#

#STILL GOING TO CHANGE DATA
def fetch(city, cuisine, day, time):
	#time format: 00:00-00:00
	#All data must be in CamelCase
	time = time.split('-')
	day = day.lower()
	cypher = "MATCH (rest:Business)-[:IN_CATEGORY]->(Category {id: '%s'}) WHERE rest.city='%s' AND rest.%sStart>'%s' AND rest.%sEnd<'%s' RETURN rest"%(cuisine, city, day, time[0], day, time[1])
	return graph.run(cypher).data()		#RETURNS list of dictionaries

def get_reviews(restaurant): #dict object
	id = restaurant.get('id')
	cypher = "MATCH (:Business {id : '%s'})<-[r:REVIEWS]-(:User) RETURN r"%(id)
	return graph.run(cypher).data()

def get_user_from_review(text): #property eg id, text... =  property_val
	cypher = "MATCH (u:User)-[r:Reviews]->(:Business) WHERE r.text='%s' RETURN u"%(text)
	return graph.run(cypher).data()[0] #This should work...

def get_social_circle(user):
	id = user.get('id')
	cypher = "MATCH (u:User {id : '%s'})-[:FRIEND*1..2]->(b:User) RETURN b"%(id)
#sorts and finds which restaurant to recommend

#eSlOI3GhroEtcbaD_nFXJQ
def get_reviews_by_50(users, city, cuisine): #users are list of dict, other are strings
	full_list = list()
	for user in users:
		id = user.get('id')
		cypher = "MATCH (:User {id : '%s')-[r:REVIEWS]->(:Business) RETURN r"%(id)
		temp_list = graph.run(cypher).data()
		full_list = full_list + temp_list

	return full_list

#--------------------------------------------------------------------------------#
#	ADAM & JOHAN
#--------------------------------------------------------------------------------#

#Sort by stars, tie break by review count
def recommend_rest(restaurants): #restaurants is list of dictionaries
	sorted_list  = sorted(restaurants, reverse= True, key= lambda k: (k['stars'],k['review_count']))
	return sorted_list[0]

def get_top_review(reviews): #list of dictionaries
	sorted_list = sorted(reviews, reverse= True, key= lambda k: (k['useful']) )
	return sorted_list[0]

#sort by highest review count
def get_50_reviewers(users):
	s = 'temp'
def filter_reviews(reviews):
	s = 'temp'
#--------------------------------------------------------------------------------#
#	SARAH
#--------------------------------------------------------------------------------#

def get_input():
	global city
	city = 'sdsdf' #etc...

#information all within the dict object
def display_stats(restaurant):
	name = restaurant.get('name')
	#full address
	stars = restaurant.get('stars')
	#review_count = restaurant.get('review_count')

def display_useful_review(review, user): #review and user are dicts
	#full text
	#name of user
	#stars
	s = 'tempo'
def display_photos(restaurant):
	s = restaurant
#--------------------------------------------------------------------------------#
#	RUN
#--------------------------------------------------------------------------------#
def main():
	open_graph()

	#Part 1: Recommend a restaurant with it's review
	get_input()

	#TEST CODE#
	city = 'New York'
	cuisine = ''
	day = ''
	time = '0-0'
	##

	rest_results = fetch(city, cuisine, day, time) #rest_results is a list of dicts
	restaurant = recommend_rest(rest_results) #restaurant should be a dict object
	
	reviews_result = get_reviews(restaurant) #list of dictionaries
	top_review = get_top_review(reviews_result) #dict object
	top_review_user = get_user_from_review(top_review.get('text'))
	
	# Part 2: Recommend 5 more restaurants based on 50 other users
	circle = get_social_circle(top_review_user) #circle is list of dicts

	top_50  = get_50_reviewers(circle) #top_50 list of dict
	reviews_by_50 = get_reviews_by_50(top_50, city, cuisine) #list of dict
	top_5_restaurants = filter_reviews(reviews_by_50) #list of dict
	
	#Part 3: Display information

	display_stats(restaurant)
	display_useful_review(top_review, top_review_user)
	display_photos(restaurant)

	for restaurant in top_5_restaurants:
		display_stats(restaurant)


if __name__ == '__main__':
	main()
