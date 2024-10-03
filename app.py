

from flask import Flask, jsonify, make_response, request 

app = Flask(__name__)

# @app.route("/", methods=["GET"])
# def index():
#     return make_response("<h1>Hello world</h1>", 200)

# if __name__ == "__main__":
#     app.run(debug=True)



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

@app.route("/api/v1.0/businesses", methods=["GET"])
def show_all_businesses():
    return make_response( jsonify( businesses ), 200 )

@app.route("/api/v1.0/businesses/<int:id>", methods=["GET"])
def show_one_business(id):
    data_to_return =  [ business for business in businesses if business['id'] == id ]
    return make_response( jsonify(  data_to_return[0] ), 200 )

@app.route("/api/v1.0/businesses", methods=["POST"])
def add_business():
    next_id = businesses[-1]["id"] + 1
    new_business = { 
        "id" : next_id,
        "name" : request.form["name"],
        "town" : request.form["town"],
        "rating" : request.form["rating"],
        "reviews" : []
    }
    businesses.append(new_business)
    return make_response( jsonify( new_business ), 201)

if __name__ == "__main__":
    app.run(port=8000, debug=True)
