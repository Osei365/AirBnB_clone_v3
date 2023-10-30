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
def places_search():
    """
    Retrieves all Place objects depending of the JSON in the body
    of the request
    """

    if request.get_json() is None:
        abort(400, description="Not a JSON")

    data = request.get_json()
    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    if data is None or not (states or cities or amenities):
        places = storage.all(Place).values()
        result = [place.to_dict() for place in places]
        return jsonify(result)

    the_place = []
    if states:
        the_state = [storage.get(State, the_id) for the_id in states]
        for state in the_state:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            the_place.append(place)

    if cities:
        city_places = [storage.get(City, city_id) for city_id in cities]
        for city in city_places:
            if city:
                for place in city.places:
                    if place not in the_place:
                        the_place.append(place)

    if amenities:
        if not the_place:
            the_place = storage.all(Place).values()
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
        the_place = [place for place in the_place
                     if all([am in place.amenities
                            for am in amenities_obj])]
    places = []
    for p in the_place:
        d = p.to_dict()
        d.pop('amenities', None)
        places.append(d)

    return jsonify(places)
