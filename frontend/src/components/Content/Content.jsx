import PropTypes from "prop-types";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import "./Content.css";

const ContentModule = ({ responseMessage }) => {
    return (
        <div className="content-module">
            <div className="response-box">
                {responseMessage ? (
                    <ReactMarkdown
                        className="response-text"
                        remarkPlugins={[remarkGfm]}
                    >
                        {responseMessage}
                    </ReactMarkdown>
                ) : (
                    <p className="placeholder-text">
                        Submit an image to see the response here.
                    </p>
                )}
            </div>
        </div>
    );
};

ContentModule.propTypes = {
    responseMessage: PropTypes.string,
};

export default ContentModule;
