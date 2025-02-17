
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Sidebar from '../components/common/Sidebar';
import axios from '../utils/axiosConfig';
import DocTabs from '../components/DocTabs';
import FileViewer from '../components/FileViewer';
import '../styles/pages/DocumentDashboard.css';

const CaseDashboard = () => {
    const { caseId , fileId } = useParams();
    const [activeTab, setActiveTab] = useState('documents');
    const [fileUrl, setFileUrl] = useState("");
    const [jsonData, setJsonData] = useState({});
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchAnalysis = async () => {
            //try to fet analysis through file id
            try{
                const response = await axios.get(`http://localhost:8000/api/api/get-analysis/${fileId}/`);
                setFileUrl(response.data.file_url);
                setJsonData(response.data.json_data);
                setLoading(false);
            } catch (error) {
                console.error("Error while fetching analysis", error);
                setLoading(false);
            }
        };

        fetchAnalysis();
    }, [fileId]);

    return (
        <div className="document-dashboard">
            <Sidebar />
            <div className="main-content">
                <header className="header">
                    <h2>File Number: {fileId} Case Number: {caseId}</h2>
                </header>
                <DocTabs fileId={fileId} activeTab="summary" />
                <div className="document-content">
                    
                    <section className="file-viewer-section">
                        <FileViewer fileUrl={fileUrl}/>
                    </section>

                    <section className='document-summary'>
                        <p>this is where the document summary will go.</p>
                    </section>
                    
                </div>
            </div>
        </div>
    );
};

export default CaseDashboard;
