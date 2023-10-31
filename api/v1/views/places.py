#!/usr/bin/python3
"""returns a json string"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.place import Place
from models.user import User
from models.city import City
from models.amenity import Amenity


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


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def place_search():
    json_dict = request.get_json()
    if json_dict is None:
        abort(400, 'Not a JSON')

    result = []
    states_list = json_dict.get('states', [])
    city_lists = json_dict.get('cities', [])
    amenity_lists = json_dict.get('amenities', [])
    all_keys = (states_list or city_lists or amenity_lists)

    if json_dict is None or not all_keys:
        places = storage.all(Place)
        result.extend([obj.to_dict() for obj in places.values()])
        return jsonify(result)

    if states_list:
        for state_id in states_list:
            state = storage.get(State, state_id)
            if state:
                for c in state.cities:
                    if c:
                        for place in c.places:
                            result.append(place)

    if city_lists:
        for city_id in city_lists:
            c = storage.get(City, city_id)
            if c:
                for place in c.places:
                    if place not in result:
                        result.append(place)

    if amenity_lists:
        if len(result) == 0:
            result = storage.all(Place).values()
        amenities = [storage.get(Amenity, a_id) for a_id in amenity_lists]
        new_result = []
        for place in result:
            if all([am in place.amenities for am in amenities]):
                new_result.append(place)
        result = new_result.copy()
    places = [place.to_dict() for place in result]
    return jsonify(places)
