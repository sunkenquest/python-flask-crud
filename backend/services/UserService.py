from datetime import timedelta
import cryptography
from flask_jwt_extended import create_access_token
from utils.utils import decrypt_password, encrypt_password
from models.UserModel import User
from config import db


class UserService:
    def check_user_exist(self, arg, value):
        """Check if a user with a specific username or email exists"""
        existing_user = User.query.filter_by(**{arg: value}).first()

        if existing_user:
            return existing_user

        return None

    def create_access_token(self, user):
        access_token = create_access_token(
            identity={"user_id": user.id, "username": user.username},
            expires_delta=timedelta(days=1),
        )

        return access_token

    def authenticate_user(self, username, password):
        """Authenticate the user by decrypting the password and checking credentials"""
        user = self.check_user_exist("username", username)

        if not user:
            return None, {"msg": "User not found"}, 404

        try:
            decrypted_password = decrypt_password(user.password)
        except cryptography.fernet.InvalidToken:
            return None, {"msg": "Error decrypting stored password"}, 500

        if decrypted_password != password:
            return None, {"msg": "Invalid credentials"}, 401

        access_token = self.create_access_token(self, user)

        return access_token, None, 200

    def register_user(self, username, password, email):
        """Register a new user by saving their credentials to the database"""
        encrypted_password = encrypt_password(password)

        new_user = User(username=username, password=encrypted_password, email=email)

        try:
            db.session.add(new_user)
            db.session.commit()

            return {"msg": "User registered successfully"}, 201
        except Exception as e:
            db.session.rollback()
            return {"msg": "Error saving user", "error": str(e)}, 500
