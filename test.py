from py2neo import Graph

	
def open_graph():
	uri = "bolt://neo4j:payR900chump@localhost:8000"
	return Graph(uri)

def main():
	graph = open_graph()

	nodes = graph.run('MATCH (rest:Business) RETURN rest LIMIT 15').data()
	for node in nodes:
			print(node)
			print()
if __name__ == '__main__':
	main()

