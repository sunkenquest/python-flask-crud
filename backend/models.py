from config import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), unique=False, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)

    @property
    def to_json(self):
        return {
            "id": self.id,
            "username": self.user_name,
            "password": self.password,
        }
