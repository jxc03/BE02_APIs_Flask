

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
    if id in businesses:
        return make_response( jsonify(  businesses[id] ), 200 )
    else: 
        return make_response( jsonify( {"error" : "Invalid business ID"} ), 404)

#Need to check over
#Adding new element
@app.route("/api/v1.0/businesses", methods=["POST"]) #Route route
def add_business(): #Defines function
    
    #If all required fields are present 
    if  "name" in request.form and \
        "town" in request.form and \
        "rating" in request.form:

        #Validation if 'name' is a string and not empty
        name = request.form["name"] #Gets the 'name' from data submitted
        if not isinstance(name, str) or not name.strip(): #Checks if 'name' is not a string or empty
            return make_response( jsonify( {"error" : "Missing business name"} ), 404) #Returns error if invalid with 404 status 

        #Validation if 'town' is a string and not empty
        town = request.form["town"] #Gets the 'town' from data submitted
        if not isinstance(name, str) or not town.strip(): #Checks if 'town' is not a string or empty
            return make_response( jsonify ( {"error" : "Missing town"} ), 404) #Returns error if invalid with 404 status

        #Validation if 'rating' is a between 1 and 5 and an integer
        try: 
            rating = int(request.form["rating"]) #Gets the 'rating' from data submitted and converts to integer
            if rating not in range(1, 6): #Checks if rating is not between 1 and 5
                return make_response( jsonify ( {"error": "Rating must be between 1 and 5"} ), 404) #Returns error if invalid with 404 status
        except ValueError:
            return make_response( jsonify ( {"error": "Rating must be an integer"} ), 404) #Returns error if invalid with 404 status

        #Creates a ID for the new business
        next_id = str(uuid.uuid1()) #businesses[-1]["id"] + 1

        #Creates the new business
        new_business = { 
            "id" : next_id,
            "name" : request.form["name"],
            "town" : request.form["town"],
            "rating" : request.form["rating"],
            "reviews" : {}
        }
    
        #Adds the new business to the dictionary
        businesses[next_id] = new_business #Uses 'next_id' as the key to add new business to businesses dictionary
        return make_response( jsonify( {next_id : new_business} ), 201) #Returns the new business data with 201 status
    else:
        return make_response( jsonify( {"error" : "Missing form data"} ), 404) #Returns error message if invalide with 404 status 


'''
A further level of error trapping might be to test the type and range of each
parameter to check that (for example) the rating is an integer between 1 and 5.
This level of checking is left for you to complete as an exercise.

1. 
rating = int(request.form["rating"])
if rating not in range(1, 6)
'''

#Editing an element (business)
@app.route("/api/v1.0/businesses/<string:id>", methods=["PUT"]) #Root route
def edit_business(id): #Defines function, takes id as input
    
    #Validation if there are fields to update
    if not any(field in request.form for field in ["name", "town", "rating"]): #Checks if there is no data in field to update
        return make_response( jsonify ( {"error" : "There is no fields to update"} ), 404) #Returns error if no fields are provided with 404 status

    #Validation if business ID exists in businesses dictionary
    if id not in businesses: #Checks if there is no matching ID
        return make_response( jsonify ( {"error" : "Invalid business ID"} ), 404) #Returns error if ID doesn't match to ID in dictionary
    
    #Validation for 'name'
    if "name" in request.form:  #Checks if 'name' is provided
        name = request.form["name"].strip() #Gets 'name' and strips whitespace
        #Validate the name
        if not name or not name.isalpha(): #Checks if 'name' is not empty and is a string
            return make_response( jsonify ( {"error": "Name must be a string and not empty"} ), 404) #Returns error if 'name' is not a string or empty with 404 status
        businesses[id]["name"] = name  #Updates the name of the business

    #Validation for 'town'
    if "town" in request.form: #Checks if 'town' is provided
        town = request.form["town"].strip() #Gets 'town'and strips whitespace
        #Validate the town
        if not town or not town.isalpha: #Checks if 'town' not empty and is a string
            return make_response( jsonify ( {"error": "Town must be a string and not empty"} ), 404) #Returns error if 'town' is not a string or empty with 404 status
        businesses[id]["town"] = town #Updates the town of the business

    #Validation for 'rating'
    if "rating" in request.form: #Checks if 'rating' is provided
        try:
            rating = int(request.form["rating"]) #Converts rating to integer
            if rating in range(1, 6): #Checks if rating is between 1 and 5
                businesses[id]["rating"] = rating #Updates the rating of the business
            else:
                return make_response( jsonify ( {"error": "Rating must be between 1 and 5"} ), 404) #Returns error if rating is not between 1 and 5 with 404 status
        except ValueError:
            return make_response( jsonify ( {"error": "Rating must be an integer"} ), 404) #Returns error if rating is not a number with 404 status
                
    return make_response(jsonify (businesses[id]), 200) #Returns the updated business data with 200 status

#Deleting an element
@app.route("/api/v1.0/businesses/<string:id>", methods=["DELETE"])
def delete_business(id):
    if id in businesses:
        del businesses[id]
        return make_response(jsonify ({}), 200)
    else:
        return make_response(jsonify ({"error" : "Invalid business ID"}), 404)

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
