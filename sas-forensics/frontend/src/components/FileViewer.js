import React from 'react';
import '../styles/components/FileViewer.css';

const FileViewer = ({ fileUrl }) => {
    return (
        <div className="file-viewer">
            {fileUrl ? (
                <iframe
                    src={fileUrl}
                    title="File Viewer"
                    width="100%"
                ></iframe>
            ) : (
                <p>No file selected</p>
            )}
        </div>
    );
};

export default FileViewer;
