from py2neo import Graph
from flask import Flask, render_template, request, redirect, url_for
import passw

username = "neo4j"
password = passw.ord()
uri = "bolt://" + username + ":" + password + "@localhost:8000"
graph = Graph(uri)



def fetch(city, cuisine, day, time):
    #TODO add day and time to query
    day = day.lower()
    cypher = "  MATCH (rest:Business)-[:IN_CATEGORY]->(Category {id: '%s'})\
                WHERE rest.city =~ '(?i)%s'\
                WITH rest ORDER BY rest.stars DESC\
                RETURN rest, size((rest)<-[:REVIEWS]-()) AS rev_count"%(cuisine, city)
    return graph.run(cypher).data()

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


def recommend_rest(restaurants):
    if len(restaurants) == 0:
        return

    top_rest = restaurants[0]

    for rest in restaurants:
        if float(rest['rest']['stars']) < float(top_rest['rest']['stars']):
            break
        elif rest['rev_count'] > top_rest['rev_count']:
             top_rest = rest
    return top_rest

app = Flask(__name__)

@app.route("/search", methods=["GET"])
def search():
    city = request.args.get("city")
    cuisine = request.args.get("cuisine")
    restaurant = recommend_rest(fetch(city, cuisine, "", ""))
    if (restaurant == None):
        rest_found = False
        rest_name = ""
        stars = 0
        review_count = 0
    else:
        rest_found = True;
        rest_name = restaurant['rest']['name']
        stars = restaurant['rest']['stars']
        review_count = restaurant['rev_count']
    return render_template("search.html", found=rest_found, rest=rest_name,
    stars=stars, review_count=review_count)

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
