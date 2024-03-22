from flask import request,  Blueprint
from flask.json import jsonify
from queries.get import isBlackListed
from commands.create import CreateBlackList
from errors.errors import IvalidDataError

blacklist_blueprint = Blueprint("blacklist", __name__)

@blacklist_blueprint.route("/blacklists", methods=["POST"])
def create():
    try:
        data = request.get_json()
        headers = request.headers
        ipAddres = request.remote_addr
        result = CreateBlackList(data, ipAddres, headers).execute()
        return jsonify({'id': result.id, 'createdAt': str(result.createdAt)}), 200
    except IvalidDataError:
        return "", 409


@blacklist_blueprint.route("/blacklists/<string:email>", methods=["GET"])
def get(email):
    headers = request.headers   
    response = isBlackListed(email, headers).query()
    return jsonify({'isBlacklisted': response["isblocked"], 'blocked_reason': response["blocked_reason"]}), 200

@blacklist_blueprint.route("/", methods=["GET"])
def healthcheck():
    return jsonify({'status': 'UP'})
