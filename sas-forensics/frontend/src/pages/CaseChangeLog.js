import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Sidebar from '../components/common/Sidebar';
import axios from '../utils/axiosConfig';
import CaseTabs from '../components/CaseTabs';
import '../styles/pages/CaseChangeLog.css';

const CaseChangeLog = () => {
    const { caseId } = useParams();
    const [changeLog, setChangeLog] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchChangeLog = async () => {
            try {
                const response = await axios.get(`/api/cases/${caseId}/change-log/`);
                setChangeLog(response.data);
            } catch (err) {
                console.error('Error fetching change log:', err);
                setError('Failed to load the change log. Please try again later.');
            } finally {
                setLoading(false);
            }
        };

        fetchChangeLog();
    }, [caseId]);

    const renderTableContent = () => {
        if (loading) {
            return <p>Loading change log...</p>;
        }

        if (error) {
            return <p className="error">{error}</p>;
        }

        if (changeLog.length === 0) {
            return <p className="no-data">No changes found for this case.</p>;
        }

        return (
            <table className="change-log-table" aria-label="Case Change Log">
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
        <div className="case-change-log">
            <Sidebar />
            <div className="main-content">
                <header>
                    <h1>Case Change Log</h1>
                    <h2>Case ID: {caseId}</h2>
                </header>

                <CaseTabs caseId={caseId} activeTab="dashboard" />
                <div className="content-section">{renderTableContent()}</div>
            </div>
        </div>
    );
};

export default CaseChangeLog;
