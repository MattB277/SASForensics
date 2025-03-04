import React, { useState } from 'react';
import axios from '../utils/axiosConfig';
import '../styles/components/FileUpload.css';

const FileUpload = ({ caseId, onClose, onFileUploaded }) => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [uploadStatus, setUploadStatus] = useState('');
    const [uploadProgress, setUploadProgress] = useState(0);

    const handleFileChange = (e) => {
        setSelectedFile(e.target.files[0]);
        setUploadStatus('');
        setUploadProgress(0);
    };

    const handleUpload = async () => {
        if (!selectedFile) {
            setUploadStatus('Please select a file.');
            return;
        }

        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('case_id', caseId);

        try {
            const response = await axios.post('/files/', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
                onUploadProgress: (progressEvent) => {
                    const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                    setUploadProgress(percentCompleted);
                },
            });
            setUploadStatus('File uploaded successfully.');
            setSelectedFile(null);
            if (onFileUploaded) onFileUploaded();
        } catch (error) {
            console.error('Upload failed:', error);
            setUploadStatus('Failed to upload. Try again.');
        }
    };

    return (
        <div className="file-upload-modal">
            <div className="file-upload-content">
                <h3>Upload a File</h3>
                <input type="file" onChange={handleFileChange} />
                {selectedFile && <p>Selected File: {selectedFile.name}</p>}

                {uploadProgress > 0 && (
                    <div className="progress-bar">
                        <div className="progress-bar-filled" style={{ width: `${uploadProgress}%` }} />
                    </div>
                )}

                <div className="actions">
                    <button onClick={handleUpload}>Upload</button>
                    <button onClick={onClose}>Close</button>
                </div>

                {uploadStatus && <p className="upload-status">{uploadStatus}</p>}
            </div>
        </div>
    );
};

export default FileUpload;
