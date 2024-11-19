from datetime import timedelta
import cryptography
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

from services.UserService import UserService
from models.UserModel import User
from config import db
from utils.utils import encrypt_password, decrypt_password

user_bp = Blueprint("user", __name__)
user_service = UserService()


@user_bp.route("/login", methods=["POST"])
def login():
    """
    Authenticate a user by checking their credentials.
    """
    username = request.json.get("username")
    password = request.json.get("password")

    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400

    user = user_service.check_user_exist("username", username)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    access_token, error, status_code = user_service.authenticate_user(
        username, password
    )

    if error:
        return jsonify(error), status_code

    return jsonify({"access_token": access_token}), status_code


@user_bp.route("/register", methods=["POST"])
def register():
    """
    Register a new user by saving their credentials to the database.
    """
    username = request.json.get("username")
    password = request.json.get("password")
    email = request.json.get("email")

    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400

    existing_user = user_service.check_user_exist("username", username)
    existing_email = user_service.check_user_exist("email", email)

    if existing_user or existing_email:
        return jsonify({"msg": "User already exists"}), 409

    message, status_code = user_service.register_user(username, password, email)

    return jsonify(message), status_code
