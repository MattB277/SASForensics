import '../styles/pages/DocumentDashboard.css';

import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Sidebar from '../components/common/Sidebar';
import axios from '../utils/axiosConfig';
import DocTabs from '../components/DocTabs';

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
                        <iframe
                            src={selectedFile}
                            title="File Viewer"
                            width="100%"
                            height="100%"
                            frameBorder="0"
                        ></iframe>
                    </section>
                    <section className="documents-related">
                        <nav className="tab-bar">
                            <button
                                className={`tab ${activeTab === 'documents' ? 'active' : ''}`}
                                onClick={() => setActiveTab('documents')}
                            >
                                Documents
                            </button>
                        </nav>

                        <article className="tab-body">
                            {activeTab === 'documents' && (
                                <div className="documents">{renderDocuments()}</div>
                            )}
                        </article>
                    </section>
                </div>
            </div>
        </div>
    );
};

export default CaseDashboard;
