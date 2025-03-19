import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Sidebar from '../components/common/Sidebar';
import axios from '../utils/axiosConfig';
import '../styles/pages/Dashboard.css';
import fileImage from '../assets/cases-icon.png';

const Dashboard = () => {
    const [cases, setCases] = useState([]);
    const [documents, setDocuments] = useState([]);
    const [loadingCases, setLoadingCases] = useState(true);
    const [loadingDocs, setLoadingDocs] = useState(true);
    const [errorCases, setErrorCases] = useState(null);
    const [errorDocs, setErrorDocs] = useState(null);

    useEffect(() => {
        // Fetch Recent Cases
        axios.get('/dashboard/')
            .then(response => {
                setCases(response.data);
                setLoadingCases(false);
            })
            .catch(err => {
                console.error('Error fetching cases:', err);
                setErrorCases('Failed to load recent cases.');
                setLoadingCases(false);
            });
    
        // Fetch Recent Documents
        axios.get('/recent-documents/')  // Updated to use the new backend URL
            .then(response => {
                setDocuments(response.data);
                setLoadingDocs(false);
            })
            .catch(err => {
                console.error('Error fetching documents:', err);
                setErrorDocs('Failed to load recent documents.');
                setLoadingDocs(false);
            });
    }, []);

    const getCaseNumber = (case_id) => {
        const caseObj = cases.find(c => c.case_number === case_id);
        return caseObj ? caseObj.case_id: null; 
    };
    
    return (
        <div className="dashboard-container">
            <Sidebar />

            <div className="dashboard-content">
                <h1>Dashboard</h1>

                <div className="dashboard-grid">
                    {/* Recent Cases Section */}
                    <div className="recent-cases">
                        <h2>Your Recent Cases</h2>
                        {loadingCases ? (
                            <p>Loading cases...</p>
                        ) : errorCases ? (
                            <p className="error">{errorCases}</p>
                        ) : cases.length > 0 ? (
                            <div className="case-items-grid">
                                {cases.map(caseItem => (
                                    <div key={caseItem.case_id} className="case-item">
                                        <div className="case-header">
                                            <span
                                                className={`indicator ${
                                                    caseItem.status === 'new_evidence'
                                                        ? 'red'
                                                        : caseItem.status === 'new_collaboration'
                                                        ? 'orange'
                                                        : 'green'
                                                }`}
                                            ></span>
                                            <h3>{caseItem.case_number}</h3>
                                        </div>
                                        <p><strong>Type:</strong> {caseItem.type_of_crime}</p>
                                        <p><strong>Location:</strong> {caseItem.location}</p>
                                        <p><strong>Last Updated:</strong> {caseItem.last_updated.split('T')[0]}</p>
                                        <p>
                                            <strong>Status:</strong>{' '}
                                            <span
                                                className={
                                                    caseItem.status === 'new_evidence'
                                                        ? 'red-text'
                                                        : caseItem.status === 'new_collaboration'
                                                        ? 'orange-text'
                                                        : 'green-text'
                                                }
                                            >
                                                {caseItem.status.replace('_', ' ')}
                                            </span>
                                        </p>
                                        <Link
                                            to={`/case-dashboard/${caseItem.case_id}`}
                                            className="view-case-link"
                                        >
                                            View Case
                                        </Link>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <p>No cases available.</p>
                        )}
                    </div>

                    {/* Your Recent Documents Section */}
                    <div className="recent-documents">
                        <h2>Your Recent Documents</h2>
                        {loadingDocs ? (
                            <p>Loading documents...</p>
                        ) : errorDocs ? (
                            <p className="error">{errorDocs}</p>
                        ) : documents.length > 0 ? (
                            <div className="document-items-grid">
                                {documents.map((doc) => (
                                    <div key={doc.file_id} className="document-item">
                                        <img
                                            src={fileImage}
                                            alt="File"
                                            className="document-item-image"
                                        />
                                        {/* Display Doc */}
                                        <h4>{doc.case_id}</h4>
                                        <p>File: {doc.file_name}</p>
                                        <Link
                                            to={`/case/${getCaseNumber(doc.case_id)}/document-dashboard/${doc.file_id}`} 
                                            className="view-document-link"
                                        >
                                            View Document
                                        </Link>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <p>No recent documents available.</p>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
