#!/usr/bin/python3
"""returns a json string"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.engine.db_storage import classes


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def get_amenities():
    if request.method == 'POST':
        json_dic = request.get_json()
        if json_dic is None:
            abort(400, 'Not a JSON')
        if 'name' not in json_dic:
            abort(400, 'Missing name')
        obj = classes['Amenity'](**json_dic)
        obj.save()
        return make_response(jsonify(obj.to_dict()), 201)
    objs = storage.all('Amenity')
    new_objs = [obj.to_dict() for obj in objs.values()]
    return jsonify(new_objs)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    obj = storage.get(classes['Amenity'], amenity_id)
    if obj is not None:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    obj = storage.get(classes['Amenity'], amenity_id)
    if obj is not None:
        obj.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    obj = storage.get(classes['Amenity'], amenity_id)
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
