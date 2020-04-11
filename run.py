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
    cypher = '  MATCH (rest:Business)-[:IN_CATEGORY]->(Category {id: "%s"})\
                WHERE rest.city =~ "(?i)%s"\
                WITH rest ORDER BY rest.stars DESC\
                RETURN rest, size((rest)<-[:REVIEWS]-()) AS rev_count'%(cuisine, city)
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
	cypher = 'MATCH (:Business {id : "%s"})<-[r:REVIEWS]-(u:User)\
                RETURN r, u'%(id)
	return graph.run(cypher).data()

def get_top_review(reviews):
    #remove reviews older than 2 years
    older_reviews = []
    now = date.today()
    now_str = "%s-%s-%s"%(str(now.year-2), '{:02d}'.format(now.month),
        '{:02d}'.format(now.day))
    for i in range(len(reviews) - 1, -1, -1):
        if reviews[i]['r']['date'] < now_str:
            reviews.remove(reviews[i])
            older_reviews.append(reviews[i])
        elif reviews[i]['r']['useful'] == None:
            reviews[i]['r']['useful'] = 0
    #sort
    reviews.sort(key=lambda x: (x['r']['useful'], x['r']['date']), reverse=True)
        if reviews[0] is None :
            if older_reviews[i]['r']['useful'] == None:
                older_reviews['r']['useful'] = o
            
            older_reviews.sort(key=lambda k: (k['r']['useful'], k['r']['date'], reverse=True)) 
            return older_reviews[0]
        else
            return reviews[0]

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

def recommend_5_rest(user_id, rest_name, city, cuisine): #all params are strings
    users = get_social_circle(user_id)
    if not users:
        return

    all_reviews = get_reviews_by_50(users, rest_name, city, cuisine)

    #delete restaurants with same name
    all_reviews.sort(key=lambda x: (x['name'], x['stars']), reverse=True)
    i = 0
    while i < len(all_reviews)-1:
        while i < len(all_reviews)-1 and\
        all_reviews[i]['name'] == all_reviews[i+1]['name']:
            all_reviews.remove(all_reviews[i+1])
        i+=1

    #get top 5
    all_reviews.sort(key=lambda x: x['stars'], reverse=True)
    return all_reviews[:5]


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
    other_rests = None
    if restaurant:
        rest_name = restaurant['rest']['name']
        rest_stars = float(restaurant['rest']['stars'])
        review_count = int(restaurant['rev_count'])
        top_review = get_top_review(get_reviews(restaurant['rest']))
        if top_review:
            top_reviewer = top_review['u']['name']
            top_rev_text = top_review['r']['text']
            top_rev_stars = top_review['r']['stars']
            other_rests = recommend_5_rest(top_review['u']['id'], rest_name, city, cuisine)

    return render_template("search.html", rest=rest_name,rest_stars=rest_stars,
    review_count=review_count, top_reviewer=top_reviewer,
    top_rev_text=top_rev_text, top_rev_stars=top_rev_stars,
    other_rests=other_rests)

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
