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
                    height="800px"
                    frameBorder="0"
                ></iframe>
            ) : (
                <p>No file selected</p>
            )}
        </div>
    );
};

export default FileViewer;
