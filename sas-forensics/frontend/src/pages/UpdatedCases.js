import React, { useState, useEffect } from 'react';
import Sidebar from '../components/common/Sidebar';
import '../styles/pages/UpdatedCases.css';
import axios from '../utils/axiosConfig';

import fileIcon from '../assets/file.png';
import connectionIcon from '../assets/connection.png';
import commentIcon from '../assets/comment.png';
import casesIcon from '../assets/cases-icon.png';

const UpdatedCases = () => {
    const [newEvidence, setNewEvidence] = useState([]);
    const [newComments, setNewComments] = useState([]);
    const [newConnections, setNewConnections] = useState([]);
    const [multipleChanges, setMultipleChanges] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        axios
            .get('/updated-cases/')
            .then((response) => {
                const { evidence = [], comments = [], connections = [], groupedChanges = {} } = response.data;
                setNewEvidence(evidence);
                setNewComments(comments);
                setNewConnections(connections);
                setMultipleChanges(groupedChanges);
                setLoading(false);
            })
            .catch((err) => {
                console.error('Error fetching updated cases:', err);
                setError('Failed to load updated cases.');
                setLoading(false);
            });
    }, []);

    const renderCaseItem = (item, icon, label) => {
        return (
            item &&
            item.change_date &&
            item.case_id && (
                <div key={item.case_id} className="case-item">
                    <div className="icon">
                        <img src={icon} alt={`${label} Icon`} />
                    </div>
                    <div className="case-details">
                        <p>{item.change_details} by {item.change_author}</p>
                        <p>Case: {item.case_id}</p>
                        <p>at {item.change_date.split('T')[0]}</p>
                    </div>
                </div>
            )
        );
    };

    const renderMultipleChanges = (caseId, changes) => {
        return (
            Array.isArray(changes) &&
            changes.length > 0 && (
                <div key={caseId} className="case-item">
                    <div className="icon">
                        <img src={casesIcon} alt="Cases Icon" />
                    </div>
                    <div className="case-details">
                        <p>Multiple changes by {changes.length} users</p>
                        <p>Case: {caseId}</p>
                        <p>Last change at {changes[0].change_date.split('T')[0]}</p>
                    </div>
                </div>
            )
        );
    };

    if (loading) return <div>Loading...</div>;
    if (error) return <div className="error">{error}</div>;

    return (
        <div className="updated-cases-page">
            <Sidebar />
            <div className="updated-cases-container">
                <h2>Updated Cases (by type of update)</h2>
                <div className="columns">
                    <div className="column">
                        <h3>New Evidence</h3>
                        {newEvidence.map((evidence) => renderCaseItem(evidence, fileIcon, 'Evidence'))}
                    </div>
                    <div className="column">
                        <h3>New Comments</h3>
                        {newComments.map((comment) => renderCaseItem(comment, commentIcon, 'Comment'))}
                    </div>
                    <div className="column">
                        <h3>New Connections</h3>
                        {newConnections.map((connection) => renderCaseItem(connection, connectionIcon, 'Connection'))}
                    </div>
                    <div className="column">
                        <h3>Multiple Changes</h3>
                        {Object.entries(multipleChanges).map(([caseId, changes]) => renderMultipleChanges(caseId, changes))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default UpdatedCases;
