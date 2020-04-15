from datetime import date
import back

def recommend_rest(city, cuisine, day, time):
    restaurants = back.get_restaurants(city, cuisine)
    restaurants = get_open_rests(restaurants, day, time)
    if len(restaurants) == 0:
        return

    top_rest = restaurants[0]

    for rest in restaurants:
        if float(rest['rest']['stars']) < float(top_rest['rest']['stars']):
            break
        elif rest['rev_count'] > top_rest['rev_count']:
             top_rest = rest
    return top_rest


def get_open_rests(rests, day, time):
    open_rests = []
    day = day.lower()
    for i in rests:
        start = i['rest'][day + 'Start']
        end = i['rest'][day + 'End']
        if start == None or end == None\
            or start == 'Null' or end == 'Null':
            open_rests.append(i)
            continue
        start = start.split(':')
        start = [int(start[0]), int(start[1])]
        end = end.split(':')
        end = [int(end[0]), int(end[1])]

        if compare_time(start, end) < 0:
            if compare_time(start, time) <= 0 and compare_time(time, end) < 0:
                open_rests.append(i)
                continue
        elif compare_time(start, end) > 0:
            if compare_time(start, time) <= 0 or compare_time(time, end) < 0:
                open_rests.append(i)
                continue
        else:
            open_rests.append(i)
            continue
    return open_rests


def get_top_review(restaurant):
    if not restaurant:
        return
    reviews = back.get_reviews(restaurant)
    #remove reviews older than 2 years
    older_reviews = []
    now = date.today()
    now_str = "%s-%s-%s"%(str(now.year-2), '{:02d}'.format(now.month),
        '{:02d}'.format(now.day))
    for i in range(len(reviews) - 1, -1, -1):
        if reviews[i]['r']['useful'] == None:
            reviews[i]['r']['useful'] = 0
        if reviews[i]['r']['date'] < now_str:
            older_reviews.append(reviews[i])
            reviews.remove(reviews[i])

    if len(reviews) != 0:
        reviews.sort(key=lambda x: (x['r']['useful'], x['r']['date']), reverse=True)
        return reviews[0]
    elif len(older_reviews) != 0:
        older_reviews.sort(key=lambda k: (k['r']['useful'], k['r']['date']), reverse=True)
        return older_reviews[0]


def recommend_5_rest(user_id, rest_name, city, cuisine): #all params are strings
    users = back.get_social_circle(user_id)
    if users == []:
        return []
    all_reviews = back.get_reviews_by_50(users, rest_name, city, cuisine)

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


def get_city_list():
    cities = back.get_all_cities()
    l = [(x['City'], x['City']) for x in cities]
    return l


def get_cuisine_list():
    cuisines = back.get_all_cuisines()
    l = [(x['Cuisine']['id'], x['Cuisine']['id']) for x in cuisines]
    return l


def compare_time(time1, time2):
    # returns:
    # 0 if time1 = time2
    # -1 if time1 < time2
    # 1 if time1 > time2
    if time1[0] == time2[0]:
        if time1[1] == time2[1]:
            return 0
        if time1[1] < time2[1]:
            return -1
        return 1
    if time1[0] < time2[0]:
        return -1
    return 1
