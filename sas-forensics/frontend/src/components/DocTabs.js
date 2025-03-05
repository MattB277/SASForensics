import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import '../styles/components/DocTabs.css';

const DocTabs = ({ caseId, fileId}) => {
    const location = useLocation();

    const tabs = [
        { path: `/case-dashboard/${caseId}`, label: "Back To Case Dashboard", key: "dashboard" },
        { path: `/case/${caseId}/document-dashboard/${fileId}`, label: "Document Summary", key: "summary" },
        { path: `/case/${caseId}/document-analysis/${fileId}`, label: "Full Analysis", key: "analysis" },
        { path: `/doc-entities/${fileId}`, label: "Entities", key: "entities" },
        { path: `/doc-timeline/${fileId}`, label: "Timeline", key: "timeline" },
        { path: `/case/${caseId}/document-change-log/${fileId}`, label: "Change Log", key: "changelog" },
    ];

    return (
        <div className="tabs">
            {tabs.map((tab) => (
                <Link
                    key={tab.key}
                    to={tab.path}
                    className={`tab-button tab-link ${
                        location.pathname === tab.path ? 'active' : ''
                    }`}
                >
                    {tab.label}
                </Link>
            ))}
        </div>
    );
};

export default DocTabs;
