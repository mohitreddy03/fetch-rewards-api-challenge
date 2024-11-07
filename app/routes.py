from flask import Blueprint, request, jsonify
from .services.database import DB # the inmeomry DB Class that is managing state
# Create a blueprint, this practice helps us version api end points
v0_blueprint = Blueprint('v0', __name__)

# checks the source of the IP, used to rate limit in case we have a bad actor
def get_client_ip():
    # Extract client IP from X-Forwarded-For header
    if 'X-Forwarded-For' in request.headers:
        return request.headers['X-Forwarded-For'].split(',')[0]
    return request.remote_addr

def initialize_limiter(lim):
    global limiter
    limiter = lim
    
@v0_blueprint.errorhandler(429)
def ratelimit_handler(e):
    return jsonify(error="ratelimit exceeded", message=str(e.description)), 429

# Endpoint to process a receipt and generate an ID for it
@v0_blueprint.route('/receipts/process', methods=['POST'])
def process_receipt():
    data = request.get_json()
    receipt, err = DB.add_receipt(data)
    if err:
        return jsonify({"error": receipt}), 400
    return jsonify({"id": receipt.id}), 200

# Endpoint to retrieve points awarded for a given receipt ID
@v0_blueprint.route('/receipts/<string:id>/points', methods=['GET'])
def get_receipt_points(id):
    receipt, err = DB.get_receipt(id)
    if err:
        return jsonify({"error": receipt}), 404
    return jsonify({"points": receipt.points}), 200