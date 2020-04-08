from py2neo import Graph
from flask import Flask, render_template, request, redirect, url_for
import passw
from datetime import date

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

def get_reviews(restaurant):
	id = restaurant['id']
	cypher = "MATCH (:Business {id : '%s'})<-[r:REVIEWS]-(u:User)\
                RETURN r, u"%(id)
	return graph.run(cypher).data()

def get_top_review(reviews):
    #remove reviews older than 2 years
    now = date.today()
    now_str = "%s-%s-%s"%(str(now.year-2), '{:02d}'.format(now.month),
        '{:02d}'.format(now.day))
    for i in range(len(reviews) - 1, -1, -1):
        if reviews[i]['r']['date'] < now_str:
            reviews.remove(reviews[i])
        elif reviews[i]['r']['useful'] == None:
            reviews[i]['r']['useful'] = 0
    #sort
    reviews.sort(key=lambda x: (x['r']['useful'], x['r']['date']), reverse=True)
    if reviews:
        return reviews[0]


app = Flask(__name__)

@app.route("/search", methods=["GET"])
def search():
    city = request.args.get("city")
    cuisine = request.args.get("cuisine")
    restaurant = recommend_rest(fetch(city, cuisine, "", ""))
    rest_name = ""
    rest_stars = 0.0
    review_count = 0
    top_reviewer = ""
    top_rev_text = ""
    top_rev_stars = 0.0
    if restaurant:
        rest_name = restaurant['rest']['name']
        rest_stars = float(restaurant['rest']['stars'])
        review_count = int(restaurant['rev_count'])
        top_review = get_top_review(get_reviews(restaurant['rest']))
        if top_review:
            top_reviewer = top_review['u']['name']
            top_rev_text = top_review['r']['text']
            top_rev_stars = top_review['r']['stars']

    return render_template("search.html", rest=rest_name,rest_stars=rest_stars,
    review_count=review_count, top_reviewer=top_reviewer,
    top_rev_text=top_rev_text, top_rev_stars=top_rev_stars)

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
