import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [response, setResponse] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleFileUpload = async () => {
    if (!selectedFile) {
      setError('Please select a file to upload.');
      return;
    }

    setLoading(true);
    setError(''); // Clear any previous error messages
    setResponse(''); // Clear previous response

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('mime_type', selectedFile.type); // Automatically get mime type from the file

    try {
      // Send the request to your Flask backend at http://127.0.0.1:5000/gemini/upload
      const res = await axios.post('http://127.0.0.1:5000/gemini/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setResponse(res.data.response); // Store response from backend
    } catch (err) {
      setError('Failed to upload the file. Please try again.');
    } finally {
      setLoading(false); // Stop loading
    }
  };

  return (
    <div className="App">
      <h1>Upload Image to Gemini</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleFileUpload} disabled={loading}>
        {loading ? 'Uploading...' : 'Upload'}
      </button>

      {response && (
        <div>
          <h2>Response:</h2>
          <p>{response}</p>
        </div>
      )}

      {error && (
        <div style={{ color: 'red' }}>
          <p>{error}</p>
        </div>
      )}
    </div>
  );
}

export default App;
