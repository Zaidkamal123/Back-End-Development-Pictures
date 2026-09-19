from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for pic in data:
        if pic["id"] == id:
            return pic, 200

    return jsonify(None),404
    


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture = request.json
    all_id = []
    for pic in data:
        all_id.append(pic["id"])
    if picture["id"] in all_id :
        return {"Message": f"picture with id {picture['id']} already present"},302
    else:
        data.append(picture)
        return {"Message" : "Picture add successfully", "id":picture["id"]},201

######################################################################
# UPDATE A PICTURE
######################################################################


# @app.route("/picture/<int:id>", methods=["PUT"])
# def update_picture(id):
#     picture = request.json
#     for pic in data:
#         if pic["id"] == picture["id"] :
#             pic = picture
#             return {"Message" : "picture updated successfully", "id" : picture["id"]}
#     return {"message" : "picture not found"}, 404

@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    # get data from the json body
    picture_in = request.json

    for index, picture in enumerate(data):
        if picture["id"] == id:
            data[index] = picture_in
            return picture, 201

    return {"message": "picture not found"}, 404
######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for pic in data:
        if pic["id"] == id:
            data.remove(pic)
            return {}, 204
    return {"message": "picture not found"}, 404
