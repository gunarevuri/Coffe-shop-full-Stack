import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink, dbcreate
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
#db_drop_and_create_all()

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/', methods=['GET'])
@app.route('/drinks', methods=['GET'])
def get_drinks_short():
    list_drinks=Drink.query.all()
    formatted_drinks=[d.short() for d in list_drinks]

    return jsonify({
        'success':True,
        'drinks':formatted_drinks
        })



'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def drinks_detail(jwt):
    list_drinks=Drink.query.all()
    if list_drinks is None:
        abort(400)

    formatted_drinks=[d.long() for d in list_drinks]

    return jsonify({
            'success':True,
            'drinks':formatted_drinks
            })



'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drinks(jwt):
    body=request.get_json()

    if body is None:
        abort(404)
    try:
        new_title=body.get('title')
        new_recipe=json.dumps(body.get('recipe'))

        drink=Drink(title=new_title,recipe=new_recipe)
        drink.insert()

        # list_drinks=Drink.query.order_by(Drink.id).all()
        # formatted_drinks=[d.long() for d in formatted_drinks]
        return jsonify({
            'success':True,
            'drinks':drink.long()
            })


    except Exception as e:
        print(e)
        abort(422)




'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>',methods=['PATCH'])
@requires_auth('patch:drinks')
def update_specific_drink(jwt,id):
    try:
        drink=Drink.query.filter(Drink.id==id).one_or_none()
        if not drink:
            abort(404)
        body=request.get_json()
        for item in body.keys():
            if item=='title':
                drink.title=body['title']
            if item=='recipe':
                drink.recipe=json.dumps(body['recipe'])

        drink.update()

        return jsonify({
            'success':True,
            'drinks':[drink.long()]
            })
    except Exception as e:
        print(e)
        abort(422)




'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_specific_drink(jwt,id):
    drink=Drink.query.filter(Drink.id==id).one_or_none()
    if drink is None:
        abort(404)

    drink.delete()

    return jsonify({
        'success':True,
        'delete':(id)
        })



## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        'success':False,
        'error':404,
        'message':"resource not found"
        }), 404


'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success':False,
        'error':400,
        'message':"bad_request"
        })


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
@app.errorhandler(AuthError)
def autherror(error):
    return jsonify({
        'success': False,
        'error': error.status_code,
        'message': error.error['description']
    }), error.status_code
