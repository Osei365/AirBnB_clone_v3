#!/usr/bin/python3
"""returns a json string"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.engine.db_storage import classes


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """status of API"""
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """gets stats."""
    json_dic = {}
    json_dic['amenities'] = storage.count(classes['Amenity'])
    json_dic['cities'] = storage.count(classes['City'])
    json_dic['places'] = storage.count(classes['Place'])
    json_dic['reviews'] = storage.count(classes['Review'])
    json_dic['states'] = storage.count(classes['State'])
    json_dic['users'] = storage.count(classes['User'])
    return jsonify(json_dic)
