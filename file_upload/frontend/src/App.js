import React, { useState } from 'react';
import FileList from './components/FileList';

const App = () => {
    const [selectedFile, setSelectedFile] = useState(null);

    const handleFileSelect = (file) => {
        setSelectedFile(file);
    };

    return (
        <div>
            <FileList onFileSelect={handleFileSelect} />
            {selectedFile && (
                <div>
                    <h3>Preview: {selectedFile.name}</h3>
                    <iframe
                        src={`http://127.0.0.1:8000${selectedFile.file}`}
                        width="600"
                        height="400"
                        title="File Preview"
                    />
                </div>
            )}
        </div>
    );
};

export default App;
