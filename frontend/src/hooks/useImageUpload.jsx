import { useState } from "react";

const useImageUpload = (uploadUrl) => {
    const [responseMessage, setResponseMessage] = useState("");

    const handleSubmit = async (image) => {
        if (!image) {
            setResponseMessage("Please upload an image before submitting.");
            return;
        }

        const formData = new FormData();
        formData.append("file", image);
        formData.append("mime_type", image.type || "image/jpeg");

        try {
            const response = await fetch(uploadUrl, {
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

    return { responseMessage, handleSubmit };
};

export default useImageUpload;
