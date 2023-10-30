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
    all_keys = [len(arr) == 0 for arr in json_dict.values()]
  
    if len(json_dict) == 0 or all(all_keys):
        places = storage.all(Place)
        result.extend([obj.to_dict() for obj in places.values()])
        return jsonify(result)
      
    states_list = json_dict.get('states')
    city_lists = json_dict.get('cities')
  
    if city_lists and len(city_lists) > 0:
        for city_id in city_lists:
            city = storage.get(City, city_id)
            if city:
                result.extend([place.to_dict() for place in city.places])
              
    if states_list and len(states_list) > 0:
        for state_id in states_list:
            state = storage.get(State, state_id)
            if state:
                for c in state.cities:
                    if city_lists and c.id not in city_lists:
                        result.extend([place.to_dict() for place in c.places])
                      
    amenity_lists = json_dict.get('amenities')
    if len(result) == 0:
        places = storage.all(Place)
        result.extend([obj.to_dict() for obj in places.values()])
    new_result = result.copy()
    if amenity_lists and len(amenity_lists) > 0:
        for place_dict in new_result:
            place = storage.get(Place, place_dict['id'])
            for amenity_id in amenity_lists:
                amenity = storage.get(Amenity, aemnity_id)
                if amenity not in place.amenities:
                    result.remove(place_dict)
    places = []
    for p in result:
        dic = p.to_dict()
        dic.pop('amenities', None)
        places.append(dic)
    return jsonify(result)
