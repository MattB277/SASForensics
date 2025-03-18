
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Sidebar from '../components/common/Sidebar';
import axios from '../utils/axiosConfig';
import DocTabs from '../components/DocTabs';
import FileViewer from '../components/FileViewer';
import DisplayAnalysis from '../components/DisplayAnalysis';
import '../styles/pages/DocumentDashboard.css';

const DocumentAnalysis = () => {
    const { caseId , fileId } = useParams();
    const [fileUrl, setFileUrl] = useState("");
    const [jsonData, setJsonData] = useState({});
    const [reviewed, setReviewed] = useState(false);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchAnalysis = async () => {
            //try to get analysis through file id
            try{
                const response = await axios.get(`get-analysis/${fileId}/`);
                setFileUrl(response.data.file_url);
                setJsonData(response.data.json_data);
                setLoading(false);
                setReviewed(response.data.reviewed);
            } catch (error) {
                console.error("Error while fetching analysis", error);
                setLoading(false);
            }
        };

        fetchAnalysis();
    }, [fileId]);

    if (loading) return <p>Loading document and analysis...</p>

    return (
        <div className="document-dashboard">
            <Sidebar />
            <div className="main-content">
                <header className="header">
                    <h2>File Number: {fileId} Case Number: {caseId}</h2>
                </header>
                <DocTabs caseId={caseId} fileId={fileId} activeTab="summary" />
                
                <div className="document-content">
                    
                    <section className="file-viewer-section">
                        <FileViewer fileUrl={fileUrl}/>
                    </section>

                    <section className='document-summary-section'>
                        <DisplayAnalysis jsonData={jsonData} reviewed={reviewed} keysToDisplay={"all"} fileId={fileId}/>
                    </section>

                </div>
            </div>
        </div>
    );
};

export default DocumentAnalysis;
