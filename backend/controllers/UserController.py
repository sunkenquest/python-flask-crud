from flask import Blueprint, request, jsonify, url_for
from flask_mail import Message

from services.UserService import UserService
from config import db, mail, serializer

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

    message, status_code = user_service.check_email_confirmed(user.email)

    if status_code != 200:
        return jsonify(message), status_code

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

    if not username or not password or not email:
        return jsonify({"msg": "Username, password and email are required"}), 400

    existing_user = user_service.check_user_exist("username", username)
    existing_email = user_service.check_user_exist("email", email)

    if existing_user or existing_email:
        return jsonify({"msg": "User already exists"}), 409

    message, status_code = user_service.register_user(username, password, email)
    if status_code != 201:
        return jsonify(message), status_code

    error, status_code = user_service.generate_confirmation_token(email)
    if error:
        return jsonify(error), status_code


@user_bp.route("/delete/<id>", methods=["DELETE"])
def delete(id):
    """
    Delete user
    """

    id = request.view_args["id"]

    if not id:
        return jsonify({"msg": "ID is required"}), 400

    message, status_code = user_service.delete_user(id)

    return jsonify(message), status_code


@user_bp.route("/confirm/<token>")
def confirm_email(token):
    """
    Confirm email verification
    """
    try:
        email = serializer.loads(token, salt="email-confirmation-salt", max_age=3600)
    except:
        return "The confirmation link is invalid or has expired."

    message, status_code = user_service.email_confirmed(email)
    if status_code != 200:
        return jsonify(message), status_code

    return f"Email {email} has been confirmed!"


@user_bp.route("/resend-email", methods=["POST"])
def resend_email():
    """
    Resend email confirmation
    """

    email = request.json.get("email")
    if not email:
        return jsonify({"msg": "Username, password and email are required"}), 400

    existing_user = user_service.check_user_exist("email", email)

    if not existing_user:
        return jsonify({"msg": "User with that email is not found"}), 404

    error, status_code = user_service.generate_confirmation_token(email)
    if error:
        return jsonify(error), status_code
