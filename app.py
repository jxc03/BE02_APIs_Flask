

from flask import Flask, jsonify, make_response, request 
import uuid, random

app = Flask(__name__)

'''
 @app.route("/", methods=["GET"])
 def index():
     return make_response("<h1>Hello world</h1>", 200)

 if __name__ == "__main__":
     app.run(debug=True)
'''
     
'''
businesses =  [
    {
        "id" : 1,
        "name" : "Pizza Mountain",
        "town" : "Coleraine",
        "rating" : 5,
        "reviews" : []  
    },
    {
        "id" : 2,
        "name" : "Wine Lake",
        "town" : "Ballymoney",
        "rating" : 3,
        "reviews" : []         
    },
    {
        "id" : 3,
        "name" : "Sweet Desert",
        "town" : "Ballymena",
        "rating" : 4,
        "reviews" : []
    }
]
'''

businesses =  {}

#Generates dictionary of businesses
def generate_dummy_data():
    towns = [
        'Coleraine', 'Banbridge', 'Belfast', 'Lisburn', 
        'Ballymena', 'Derry', 'Newry', 'Enniskillen',
        'Omagh', 'Ballymoney'
    ]
    businesses_dict = {}

    for i in range(100):
        id = str(uuid.uuid1())
        name = "Biz " + str(i)
        town = towns[random.randint (0, len(towns) - 1) ]
        rating = random.randint(1, 5)
        businesses_dict[id] = {
            "name": name, 
            "town": town, 
            "rating": rating, 
            "reviews": {}
        }
    return businesses_dict

#Retrieving the entire collection
@app.route("/api/v1.0/businesses", methods=["GET"])
def show_all_businesses():
    return make_response( jsonify( businesses ), 200 )

#Retrieving a single element
@app.route("/api/v1.0/businesses/<string:id>", methods=["GET"])
def show_one_business(id):
    #data_to_return =  [ business for business in businesses if business['id'] == id ]
    return make_response( jsonify(  businesses[id] ), 200 )

#Adding new element
@app.route("/api/v1.0/businesses", methods=["POST"])
def add_business():
    next_id = str(uuid.uuid1()) #businesses[-1]["id"] + 1
    new_business = { 
        "id" : next_id,
        "name" : request.form["name"],
        "town" : request.form["town"],
        "rating" : request.form["rating"],
        "reviews" : {}
    }
    #businesses.append(new_business)
    businesses[next_id] = new_business
    return make_response( jsonify( {next_id : new_business} ), 201)

#Editing an element
@app.route("/api/v1.0/businesses/<string:id>", methods=["PUT"])
def edit_business(id):
    #for business in businesses:
        #if business["id"] == id:
    businesses[id]["name"] = request.form["name"]
    businesses[id]["town"] = request.form["town"]
    businesses[id]["rating"] = request.form["rating"]
    return make_response(jsonify ( {id : businesses[id]} ), 200)

#Deleting an element
@app.route("/api/v1.0/businesses/<string:id>", methods=["DELETE"])
def delete_business(id):
    '''
    for business in businesses:
        if business["id"] == id:
            businesses.remove(business)
            break
    '''
    del businesses[id]
    return make_response(jsonify ({}), 200)

#Retrieving sub-document collection
@app.route("/api/v1.0/businesses/<string:id>/reviews", methods=["GET"])
def fetch_all_reviews(id):
    '''
    for business in businesses:
        if business["id"] == id:
            break
    '''
    return make_response(jsonify (businesses[id]["reviews"]), 200)

#Adding new element to sub-document 
@app.route("/api/v1.0/businesses/<string:b_id>/reviews", methods=["POST"])
def add_new_review(b_id):
    '''
    for business in businesses:
        if business["id"] == b_id:
            if len(business ["reviews"] ) == 0:
                new_review_id = str(uuid.uuid1())
            else:
                new_review_id = business["reviews"][-1]["id"] + 1
    '''
    new_review_id = str(uuid.uuid1())
    new_review = {
        "id" : new_review_id,
        "username": request.form["username"],
        "comment": request.form["comment"],
        "stars": request.form["stars"]
        }
            #business["reviews"].append(new_review)
    businesses[b_id]["reviews"][new_review_id] = new_review
            #break
    return make_response(jsonify ( {new_review_id : new_review} ), 201)

#Retrieving a single element from sub-document
@app.route("/api/v1.0/businesses/<string:b_id>/reviews/<string:r_id>", methods=["GET"])
def fetch_one_review(b_id, r_id):
    for business in businesses:
        if business["id"] == b_id:
            for review in business["reviews"]:
                break
            break
    return make_response(jsonify (review), 200)

#Edit single element from sub-document 
@app.route("/api/v1.0/businesses/<string:b_id>/reviews/<string:r_id>", methods=["PUT"])
def edit_review(b_id, r_id):
    '''
    for business in businesses:
        if business["id"] == b_id:
            for review in business["reviews"]:
                if review["id"] == r_id:
                    '''
    businesses[b_id]["username"] = request.form["username"]
    businesses[b_id]["comment"] = request.form["comment"]
    businesses[b_id]["stars"] = request.form["stars"]
                    #break
    return make_response(jsonify ( {id : businesses[id]} ), 200)

#Deleting single element from sub-document
@app.route("/api/v1.0/businesses/<string:b_id>/reviews/<string:r_id>", methods=["DELETE"])
def delete_review(b_id, r_id):
    '''
    for business in businesses:
        if business["id"] == b_id:
            for review in business["reviews"]:
                if review["id"] == r_id:
                    business["reviews"].remove(review)
                    break
            break
    '''
    del businesses[b_id]["reviews"][r_id]
    return make_response(jsonify ({}), 200)

if __name__ == "__main__":
    businesses = generate_dummy_data()
    app.run(port=8000, debug=True)
