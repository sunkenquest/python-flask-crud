import PropTypes from "prop-types";
import "./Content.css";

const ContentModule = ({ responseMessage }) => {
    return (
        <div className="content-module">
            <h2>Response</h2>
            <div className="response-box">
                <p className={`response-text ${responseMessage ? "" : "placeholder-text"}`}>
                    {responseMessage || "Submit an image to see the response here."}
                </p>
            </div>
        </div>
    );
};

ContentModule.propTypes = {
    responseMessage: PropTypes.string,
};

export default ContentModule;
