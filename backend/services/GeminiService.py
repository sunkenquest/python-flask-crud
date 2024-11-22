import os
import google.generativeai as genai


class GeminiService:
    def __init__(self):
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])

        self.generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        self.model = genai.GenerativeModel(
            model_name="learnlm-1.5-pro-experimental",
            generation_config=self.generation_config,
        )

    def upload_file_to_gemini(self, file_path, mime_type=None):
        """Uploads a file to Google Gemini."""
        try:
            file = genai.upload_file(file_path, mime_type=mime_type)
            return file
        except Exception as e:
            raise RuntimeError(f"Failed to upload file to Gemini: {str(e)}")

    def generate_chat_response(self, file, prompt):
        """
        Creates a chat session with Gemini and generates a response based on the prompt.
        """
        try:
            chat_session = self.model.start_chat(
                history=[
                    {
                        "role": "user",
                        "parts": [
                            file,
                            prompt,
                        ],
                    }
                ]
            )
            response = chat_session.send_message(prompt)
            return response.text
        except Exception as e:
            raise RuntimeError(f"Failed to generate chat response: {str(e)}")
