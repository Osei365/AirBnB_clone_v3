#!/usr/bin/python3
"""place and amenities."""

from flask import jsonify, make_response, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity

@app_views.route('/places/<place_id>/amenities', methods =['GET'],
                 strict_slashes=False)
def get_amenities_by_places(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenities = [obj.to_dict() for obj in place.amenities]
    return jsonify(amenities)

@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def delete_amenities_by_place(place_id, amenity_id):
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    place.amenities.remove(amenity)
    storage.save()
    return jsonify({})

@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_amenities_by_place(place_id, amenity_id):
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict())
    place.amenities.append(amenity)
    return make_response(jsonify(amenity.to_dict()), 201)
