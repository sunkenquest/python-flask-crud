from datetime import timedelta
import cryptography
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

from models.UserModel import User
from config import db
from utils.utils import encrypt_password, decrypt_password

user_bp = Blueprint("user", __name__)


@user_bp.route("/login", methods=["POST"])
def login():
    """
    Authenticate a user by checking their credentials.
    """
    username = request.json.get("username")
    password = request.json.get("password")

    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400

    user = User.query.filter_by(user_name=username).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404

    try:
        decrypted_password = decrypt_password(user.password)
    except cryptography.fernet.InvalidToken:
        return jsonify({"msg": "Error decrypting stored password"}), 500

    if decrypted_password != password:
        return jsonify({"msg": "Invalid credentials"}), 401

    access_token = create_access_token(
        identity={"user_id": user.id, "username": user.user_name},
        expires_delta=timedelta(days=1),
    )

    return jsonify({"access_token": access_token}), 200


@user_bp.route("/register", methods=["POST"])
def register():
    """
    Register a new user by saving their credentials to the database.
    """
    username = request.json.get("username")
    password = request.json.get("password")

    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400

    existing_user = User.query.filter_by(user_name=username).first()
    if existing_user:
        return jsonify({"msg": "User already exists"}), 409

    encrypted_password = encrypt_password(password)

    new_user = User(user_name=username, password=encrypted_password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"msg": "User registered successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Error saving user", "error": str(e)}), 500
