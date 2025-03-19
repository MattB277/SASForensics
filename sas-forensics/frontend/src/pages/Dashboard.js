import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Sidebar from '../components/common/Sidebar';
import axios from '../utils/axiosConfig';
import '../styles/pages/Dashboard.css';

const Dashboard = () => {
    const [cases, setCases] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        axios
            .get('/dashboard/')
            .then((response) => {
                setCases(response.data);
                setLoading(false);
            })
            .catch((err) => {
                console.error('Error fetching cases:', err);
                setError('Failed to load recent cases.');
                setLoading(false);
            });
    }, []);

    return (
        <div className="dashboard-container">
            <Sidebar />

            <div className="dashboard-content">
                <h1>Dashboard</h1>

                <div className="dashboard-grid">
                    <div className="recent-cases">
                        <h2>Your Recent Cases</h2>
                        {loading ? (
                            <p>Loading cases...</p>
                        ) : error ? (
                            <p className="error">{error}</p>
                        ) : cases.length > 0 ? (
                            <div className="case-items-grid">
                                {cases.map((caseItem) => (
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
                        <div className="legend">
                            <p>
                                <span className="indicator red"></span> New evidence
                            </p>
                            <p>
                                <span className="indicator orange"></span> New collaboration
                            </p>
                            <p>
                                <span className="indicator green"></span> No changes
                            </p>
                        </div>
                    </div>

                    <div className="quick-links">
                        <h2>Quick Links</h2>
                        <div className="links-grid">
                            <div className="link-item">
                                <div className="icon uploads"></div>
                                <p>Your Uploads</p>
                            </div>
                            <div className="link-item">
                                <div className="icon cases"></div>
                                <p>Your Cases</p>
                            </div>
                            <div className="link-item">
                                <div className="icon manage"></div>
                                <p>Manage Cases</p>
                            </div>
                            <div className="link-item">
                                <div className="icon updated"></div>
                                <p>Updated Cases</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
