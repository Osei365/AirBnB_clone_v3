#!/usr/bin/python3
"""returns a json string"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.engine.db_storage import classes


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def get_users():
    if request.method == 'POST':
        json_dic = request.get_json()
        if json_dic is None:
            abort(400, 'Not a JSON')
        if 'email' not in json_dic:
            abort(400, 'Missing email')
        if 'password' not in json_dic:
            abort(400, 'Missing password')
        obj = classes['User'](**json_dic)
        obj.save()
        return make_response(jsonify(obj.to_dict()), 201)
    objs = storage.all('User')
    new_objs = [obj.to_dict() for obj in objs.values()]
    return jsonify(new_objs)


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def get_user(user_id):
    obj = storage.get(classes['User'], user_id)
    if obj is not None:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    obj = storage.get(classes['User'], user_id)
    if obj is not None:
        obj.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    obj = storage.get(classes['User'], user_id)
    if obj is None:
        abort(404)
    json_dict = request.get_json()
    if json_dict is None:
        abort(400, 'Not a JSON')
    for key, value in json_dict.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 200)
