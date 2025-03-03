
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Sidebar from '../components/common/Sidebar';
import axios from '../utils/axiosConfig';
import DocTabs from '../components/DocTabs';
import '../styles/pages/DocumentChangeLog.css';

const DocumentChangeLog = () => {
    const { caseId, fileId } = useParams();
    const [changeLog, setChangeLog] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchChangeLog = async () => {
            try {
                const response = await axios.get(`/files/${fileId}/change-log/`);
                setChangeLog(response.data);
            } catch (err) {
                console.error('Error fetching change log:', err);
                setError('Failed to load the change log. Please try again later.');
            } finally {
                setLoading(false);
            }
        };

        fetchChangeLog();
    }, [fileId]);

    if (loading) return <p>Loading Changelog...</p>

    
    const renderTableContent = () => {
        if (loading) {
            return <p>Loading change log...</p>;
        }

        if (error) {
            return <p className="error">{error}</p>;
        }

        if (changeLog.length === 0) {
            return <p className="no-data">No changes found for this document.</p>;
        }

        return (
            <table className="change-log-table" aria-label="Document Change Log">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Type of Change</th>
                        <th>Details</th>
                        <th>Changed By</th>
                    </tr>
                </thead>
                <tbody>
                    {changeLog.map((change, index) => (
                        <tr key={index}>
                            <td>{new Date(change.change_date).toLocaleDateString()}</td>
                            <td>{change.type_of_change}</td>
                            <td>{change.change_details}</td>
                            <td>{change.change_author || 'Unknown'}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        );
    };

    return (
        <div className="document-dashboard">
            <Sidebar />
            <div className="main-content">
                <header className="header">
                    <h2>File Number: {fileId} Case Number: {caseId}</h2>
                </header>
                <DocTabs caseId={caseId} fileId={fileId} activeTab="summary" />
                
                <div className="document-content">
                    
                    <div className='document-changelog'>
                        {renderTableContent()}
                    </div>

                </div>
            </div>
        </div>
    );
};

export default DocumentChangeLog;
