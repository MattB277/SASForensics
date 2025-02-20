import React, { useState, useEffect } from 'react';
import { Link, useParams } from 'react-router-dom';
import Sidebar from '../components/common/Sidebar';
import '../styles/pages/CaseDashboard.css';
import axios from '../utils/axiosConfig';
import CaseTabs from '../components/CaseTabs';

const CaseDashboard = () => {
    const { caseId } = useParams();
    const [documents, setDocuments] = useState([]);
    const [activeTab, setActiveTab] = useState('documents');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchDocuments = async () => {
            try {
                const response = await axios.get(`/api/cases/${caseId}/files/`);
                setDocuments(response.data);
            } catch (err) {
                console.error('Error fetching documents:', err);
                setError('Failed to load documents.');
            } finally {
                setLoading(false);
            }
        };

        fetchDocuments();
    }, [caseId]);

    const renderDocuments = () => {
        if (loading) {
            return <p>Loading documents...</p>;
        }

        if (error) {
            return <p className="error">{error}</p>;
        }

        if (documents.length === 0) {
            return <p>No documents available.</p>;
        }

        return documents.map((doc) => (
            <Link
                key={doc.file_id}
                to={`/case/${caseId}/document-dashboard/${doc.file_id}`}
                className="document-link"
            >
                {doc.file.split('/').pop()}
            </Link>
        ));
    };

    return (
        <div className="case-dashboard">
            <Sidebar />

            <div className="main-content">
                <header className="header">
                    <h2>Case Number: {caseId}</h2>
                </header>
                <CaseTabs caseId={caseId} activeTab="dashboard" />

                <div className="case-content">
                    <section className="file-viewer-section">
                        <p>This area needs to be developed</p>
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
