from py2neo import Graph
import passw

username = "neo4j"
password = passw.ord()
uri = "bolt://" + username + ":" + password + "@localhost:8000"
graph = Graph(uri)


def get_restaurants(city, cuisine):
    cypher = '  MATCH (rest:Business)-[:IN_CATEGORY]->(Category {id: "%s"})\
                WHERE rest.city =~ "(?i)%s"\
                WITH rest ORDER BY rest.stars DESC\
                RETURN rest, size((rest)<-[:REVIEWS]-()) AS rev_count'%(cuisine, city)
    rests = graph.run(cypher).data()
    return rests


def get_all_cuisines():
    cypher = "MATCH (c:Category)\
                WITH c ORDER BY c.id\
                RETURN c as Cuisine"
    return graph.run(cypher).data()


def get_all_cities():
    cypher = "MATCH (b:Business)\
                WITH b ORDER BY b.city\
                RETURN DISTINCT b.city AS City"
    return graph.run(cypher).data()


def get_reviews(restaurant):
	id = restaurant['rest']['id']
	cypher = 'MATCH (:Business {id : "%s"})<-[r:REVIEWS]-(u:User)\
                RETURN r, u'%(id)
	return graph.run(cypher).data()


def get_social_circle(user_id):
    cypher = 'MATCH (:User {id : "%s"})-[:FRIEND*1..2]-(u:User)-[r:REVIEWS]-(:Business)\
                RETURN u, COUNT(r)\
                ORDER BY COUNT(r) DESC\
                LIMIT 50'%(user_id)
    return graph.run(cypher).data()


def get_reviews_by_50(users, business, city, cuisine): #users are list of dict, other are strings
    full_list = list()
    for user in users:
        id = user['u']['id']
        cypher = 'MATCH (:User {id: "%s"})-[r:REVIEWS]->(b:Business {city: "%s"})\
                    -[:IN_CATEGORY]->(Category {id: "%s"})\
                    WHERE b.name <> "%s"\
                    RETURN r.stars as stars, b.name as name'%(id, city, cuisine, business)
        temp_list = graph.run(cypher).data()
        full_list = full_list + temp_list
    return full_list
