import { useState } from "react";
import ContentModule from "../Content/Content";
import useImageUpload from "../../hooks/useImageUpload";
import "./UploadImage.css";

const UploadImage = () => {
    const [image, setImage] = useState(null);
    const [preview, setPreview] = useState(null);

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

    const handleFormSubmit = () => {
        handleSubmit(image);
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
                            <button className="submit-btn" onClick={handleFormSubmit}>
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
