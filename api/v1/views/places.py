#!/usr/bin/python3
"""returns a json string"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.user import User
from models.city import City


@app_views.route('/cities/<city_id>/places',
                 methods=['GET', 'POST'], strict_slashes=False)
def get_places_by_cities(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'POST':
        json_dic = request.get_json()
        if json_dic is None:
            abort(400, 'Not a JSON')
        if 'user_id' not in json_dic:
            abort(400, 'Missing user_id')
        user = storage.get(User, json_dic.get('user_id'))
        if user is None:
            abort(404)
        if 'name' not in json_dic:
            abort(400, 'Missing name')
        place = Place(**json_dic)
        place.city_id = city_id
        place.save()
        return make_response(jsonify(place.to_dict()), 201)
    new_objs = [obj.to_dict() for obj in city.places]
    return jsonify(new_objs)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place(place_id):
    obj = storage.get(Place, place_id)
    if obj is not None:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    obj = storage.get(Place, place_id)
    if obj is not None:
        obj.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    json_dict = request.get_json()
    if json_dict is None:
        abort(400, 'Not a JSON')
    for key, value in json_dict.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 200)
