import os
import sys
import passw
from py2neo import Graph

def init_graph():
	your_password = passw.ord()
	uri = "bolt://neo4j:{}@localhost:8000".format(your_password)
	graph = Graph(uri)

	#Clean graph
	graph.evaluate("MATCH (n) DETACH DELETE n")

	#Set up key\val with APOC schema.assert
	graph.evaluate("CALL apoc.schema.assert({Category:['name']},{Business:['id'],User:['id'],Review:['id'],Photo:['id']})")

	#Load business.json, user.json and review.json respectivelu
	graph.evaluate('CALL apoc.periodic.iterate("'
               'CALL apoc.load.json(\'file:///business.json\') YIELD value RETURN value '
               '"," '
               'MERGE (b:Business{id:value.business_id}) '
               'SET b += apoc.map.clean(value, [\'business_id\',\'categories\'],[]) '
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

	graph.evaluate('CALL apoc.periodic.iterate("'
               'CALL apoc.load.json(\'file:///photo.json\') '
               'YIELD value RETURN value '
               '"," '
               'MERGE (p:Photo{id:value.photo_id}) '
               'SET p += apoc.map.clean(value, [\'business_id\',\'photo_id\'],[0]) '
               'WITH p,value.business_id as businesses '
               'UNWIND businesses as business '
               'MERGE (b:Business{id:business}) '
               'MERGE (p)-[:PHOTO_OF]->(b) '
               '",{batchSize: 100, iterateList: true});')

def main():
    if len(sys.argv) > 1:
        switch()
    init_graph()

def switch():
    #TODO BEFORE USING CHANGE PATH TO CORRECT PATH 
    print("GO FIX THE PATH FIRST")
    #os.system("mv PATH/import PATH/import2")
    #os.system("mv PATH/import1 PATH/import")
    #os.system("mv PATH/import2 PATH/import1")

if __name__ == "__main__":
    main()