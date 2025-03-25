import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Sidebar from '../components/common/Sidebar';
import axios from '../utils/axiosConfig';
import CaseTabs from '../components/CaseTabs';
import '../styles/pages/CaseSummary.css';
import DisplayAnalysis from '../components/DisplayAnalysis';

const CaseSummary = () => {
    const { caseId } = useParams();
    const [summary, setSummary] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchCaseSummary = async () => {
            try {
                const response = await axios.get(`/case-summary/${caseId}/`);
                setSummary(response.data);
            } catch (err) {
                console.error('Error fetching case summary:', err);
                setError('Failed to load the summary. Please try again later.');
            } finally {
                setLoading(false);
            }
        };

        fetchCaseSummary();
    }, [caseId]);

    
    if (loading) return <p>Loading Case Summary...</p>

    return (
        <div className="case-summary">
            <Sidebar />
            <div className="main-content">
                <header className="header">
                    <h2>Case Number: {caseId} Summary</h2>
                </header>
                <CaseTabs caseId={caseId} activeTab="summary" />
                <div>
                    <DisplayAnalysis jsonData={summary} reviewed={true} keysToDisplay={"all"} fileId={caseId}/>
                </div>
            </div>
        </div>
    );
};

export default CaseSummary;
