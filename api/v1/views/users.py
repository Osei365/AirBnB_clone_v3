#!/usr/bin/python3
"""returns a json string"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.engine.db_storage import classes


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """get the information of all user"""
    users = []
    for user in storage.all(User).values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """get user information by user_id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_user(user_id):
    """delete user by user_id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """create a new user"""
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'email' not in data:
        abort(400, description="Missing email")
    if 'password' not in data:
        abort(400, description="Missing password")
    user = User(**data)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """update a user"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
