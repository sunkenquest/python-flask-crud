import os
from flask import Blueprint, jsonify, request
import google.generativeai as genai

from services.GeminiService import GeminiService


genai.configure(api_key=os.environ["GEMINI_API_KEY"])

gemini_bp = Blueprint("gemini", __name__)
gemini_service = GeminiService()


@gemini_bp.route("/upload", methods=["POST"])
def upload():
    """
    Endpoint to upload files to Gemini and generate a response.
    """
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    uploaded_file = request.files["file"]
    if uploaded_file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    try:
        file_path = os.path.join("/tmp", uploaded_file.filename)
        uploaded_file.save(file_path)

        mime_type = request.form.get("mime_type", "application/octet-stream")
        gemini_file = gemini_service.upload_file_to_gemini(file_path, mime_type)

        prompt = (
            "I have the ingredients listed above. Suggest a list of recipes I can make for lunch. "
            "Please format each suggestion as follows:\n\n"
            "**Recipe Name**\n\n"
            "**Ingredients**\n"
            "- List each ingredient in bullet points.\n\n"
            "**Instructions**\n"
            "- Provide step-by-step cooking instructions in bullet points."
        )
        response_text = gemini_service.generate_chat_response(gemini_file, prompt)

        os.remove(file_path)
        return jsonify({"response": response_text}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
