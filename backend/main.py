from config import app, db
from controllers.UserController import user_bp
from controllers.GeminiController import gemini_bp

app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(gemini_bp, url_prefix="/gemini")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
