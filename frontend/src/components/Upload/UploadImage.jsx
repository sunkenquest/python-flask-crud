import { useState } from "react";
import ContentModule from "../Content/Content";
import useImageUpload from "../../hooks/useImageUpload";
import "./UploadImage.css";

const UploadImage = () => {
    const [image, setImage] = useState(null);
    const [preview, setPreview] = useState(null);
    const [loading, setLoading] = useState(false);  // State for loading

    const { responseMessage, handleSubmit } = useImageUpload("http://127.0.0.1:5000/gemini/upload");

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
    };

    const handleFormSubmit = async () => {
        setLoading(true);  // Set loading to true when submit is clicked
        await handleSubmit(image);
        setLoading(false); // Set loading to false once the submission is complete
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
                            <button
                                className="submit-btn"
                                onClick={handleFormSubmit}
                                disabled={loading} // Disable button when loading
                            >
                                {loading ? (
                                    <span className="loader"></span> // Show loader when loading
                                ) : (
                                    "Submit"
                                )}
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
