from config import app, db
from controllers.UserController import user_bp

app.register_blueprint(user_bp, url_prefix="/user")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
