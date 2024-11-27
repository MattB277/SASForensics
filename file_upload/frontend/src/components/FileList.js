// src/components/FileList.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const FileList = ({ onFileSelect }) => {
    const [files, setFiles] = useState([]);

    useEffect(() => {
        axios.get('http://127.0.0.1:8000/api/files/')
            .then(response => setFiles(response.data))
            .catch(error => console.error("There was an error fetching the files!", error));
    }, []);

    return (
        <div>
            <h2>Files List</h2>
            <ul>
                {files.map(file => (
                    <li key={file.id} onClick={() => onFileSelect(file)}>
                        {file.name}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default FileList;
