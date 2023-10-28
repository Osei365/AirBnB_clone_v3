#!/usr/bin/python3
"""returns a json string"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """status of API"""
    return jsonify({"status": "OK"})
