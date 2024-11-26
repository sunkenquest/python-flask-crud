import { useState } from "react";
import ContentModule from "../Content/Content";
import "./UploadImage.css";

const UploadImage = () => {
    const [image, setImage] = useState(null);
    const [preview, setPreview] = useState(null);
    const [responseMessage, setResponseMessage] = useState("");

    const handleImageUpload = (event) => {
        const file = event.target.files[0];
        if (file) {
            setImage(file);
            const reader = new FileReader();
            reader.onloadend = () => setPreview(reader.result);
            reader.readAsDataURL(file);
        }
    };

    const handleRemoveImage = () => {
        setImage(null);
        setPreview(null);
        setResponseMessage("");
    };

    const handleSubmit = async () => {
        if (!image) {
            alert("Please upload an image before submitting.");
            return;
        }

        const formData = new FormData();
        formData.append("file", image);
        formData.append("mime_type", image.type || "image/jpeg");

        try {
            const response = await fetch("http://127.0.0.1:5000/gemini/upload", {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            setResponseMessage(data.response || "No response message received.");
        } catch (error) {
            setResponseMessage(`Error: ${error.message}`);
        }
    };

    return (
        <div className="upload-container">
            <div className="upload-box">
                {preview ? (
                    <div className="preview-container">
                        <img src={preview} alt="Uploaded Preview" className="preview-image" />
                        <div className="button-group">
                            <button className="remove-btn" onClick={handleRemoveImage}>
                                Remove
                            </button>
                            <button className="submit-btn" onClick={handleSubmit}>
                                Submit
                            </button>
                        </div>
                    </div>
                ) : (
                    <label className="upload-label">
                        <input
                            type="file"
                            accept="image/*"
                            className="upload-input"
                            onChange={handleImageUpload}
                        />
                        <span className="upload-text">Click to upload an image</span>
                    </label>
                )}
            </div>
            <ContentModule responseMessage={responseMessage} />
        </div>
    );
};

export default UploadImage;
