import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import '../styles/components/CaseTabs.css';

const CaseTabs = ({ caseId }) => {
    const location = useLocation();

    const tabs = [
        { path: `/case-dashboard/${caseId}`, label: "Case Dashboard", key: "dashboard" },
        { path: `/case-summary/${caseId}`, label: "Case Summary", key: "summary" },
        { path: `/cases/${caseId}/timeline`, label: "Case Timeline", key: "timeline" },
        { path: `/manage-case/${caseId}`, label: "Manage Case", key: "manage" },
        { path: `/case-change-log/${caseId}`, label: "Change Log", key: "changelog" },
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

export default CaseTabs;
