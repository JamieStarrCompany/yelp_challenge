from py2neo import Graph
from flask import Flask, render_template, request, redirect, url_for

username = "neo4j"
password = "Boesman1"
uri = "bolt://" + username + ":" + password + "@localhost:8000"
graph = Graph(uri)



def fetch(city, cuisine, day, time):
    #TODO add day and time to query
    day = day.lower()
    cypher = "  MATCH (rest:Business)-[:IN_CATEGORY]->(Category {id: '%s'})\
                WHERE rest.city =~ '(?i)%s'\
                WITH rest ORDER BY rest.stars DESC\
                RETURN rest"%(cuisine, city)
    return graph.run(cypher).data()

#TODO get number of reviews for givin business, for now it just returns 0
def get_review_count(business_id):
    # cypher = "  MATCH (:User)-[r:REVIEWS]->(:Business {business_id:'%s'})\
    #             RETURN count(r)"%(business_id)
    # return int(graph.run(cypher).data())
    return 0

def get_all_cuisines():
    cypher = "MATCH (c:Category)\
                RETURN c as Cuisine"
    return graph.run(cypher).data()

def get_all_cities():
    cypher = "MATCH (b:Business)\
                RETURN DISTINCT b.city AS City"
    return graph.run(cypher).data()


def recommend_rest(restaurants):
    if len(restaurants) == 0:
        return

    top_rest = restaurants[0]
    top_rest_reviews = get_review_count(top_rest['rest']['business_id'])

    for rest in restaurants:
        if float(rest['rest']['stars']) < float(top_rest['rest']['stars']):
            break
        elif get_review_count(rest['rest']['business_id']) > top_rest_reviews:
             top_rest = rest
             top_rest_reviews = get_review_count(top_rest['rest']['business_id'])
    return top_rest



app = Flask(__name__)

@app.route("/search", methods=["GET"])
def search():
    city = request.args.get("city")
    cuisine = request.args.get("cuisine")
    rest_name = recommend_rest(fetch(city, cuisine, "", ""))['rest']['name']
    return render_template("search.html", rest=rest_name)

@app.route("/", methods=["POST", "GET"])
def home():
    cities = get_all_cities()
    cuisines = get_all_cuisines()
    if request.method == "POST":
        city = request.form["city"]
        cuisine = request.form["cuisine"]
        url = url_for("search") + "?city=" + city + "&cuisine=" + cuisine
        return redirect(url)
    else:
        return render_template("index.html", cities = cities, cuisines = cuisines)


if __name__ == '__main__':
    app.run(debug=True)
