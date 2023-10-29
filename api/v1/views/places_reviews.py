#!/usr/bin/python3
"""returns a json string"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.user import User
from models.city import City
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET', 'POST'], strict_slashes=False)
def get_reviews_by_places(place_id):
    place = storage.get(Place, place_id)
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
        if 'text' not in json_dic:
            abort(400, 'Missing text')
        review = Review(**json_dic)
        review.place_id = place_id
        review.save()
        return make_response(jsonify(review.to_dict()), 201)
    new_objs = [obj.to_dict() for obj in place.reviews]
    return jsonify(new_objs)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def get_review(review_id):
    obj = storage.get(Review, review_id)
    if obj is not None:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    obj = storage.get(Review, review_id)
    if obj is not None:
        obj.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    json_dict = request.get_json()
    if json_dict is None:
        abort(400, 'Not a JSON')
    for key, value in json_dict.items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(obj, key, value)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 200)
