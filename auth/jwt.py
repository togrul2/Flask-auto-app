from flask import jsonify
from flask_jwt_extended import JWTManager

jwt = JWTManager()


@jwt.expired_token_loader
def expired_token_callback(_jwt_header, _jwt_payload):
    """Custom expired token response"""
    return jsonify(error="Access token is expired!"), 401


@jwt.invalid_token_loader
def invalid_token_callback(jwt_payload):
    """Custom invalid token response"""
    return jsonify(error=jwt_payload), 401


@jwt.unauthorized_loader
def unauthorized_callback(jwt_payload):
    """Custom invalid token response"""
    return jsonify(error=jwt_payload), 401
