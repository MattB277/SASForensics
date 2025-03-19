import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Sidebar from '../components/common/Sidebar';
import FileUpload from '../components/FileUpload';
import CaseTabs from '../components/CaseTabs';
import '../styles/pages/ManageCase.css';
import axios from '../utils/axiosConfig';

const ManageCase = () => {
    const { caseId } = useParams();
    const [caseDetails, setCaseDetails] = useState({});
    const [documents, setDocuments] = useState([]);
    const [users, setUsers] = useState([]);
    const [allUsers, setAllUsers] = useState([]);
    const [isFileUploadOpen, setIsFileUploadOpen] = useState(false);

    useEffect(() => {
        axios.get(`/cases/${caseId}/`).then((response) => setCaseDetails(response.data));
        axios.get(`/cases/${caseId}/files/`).then((response) => setDocuments(response.data));
        axios.get(`/cases/${caseId}/users/`).then((response) => setUsers(response.data));
        axios.get('/users/').then((response) => setAllUsers(response.data));
    }, [caseId]);

    const assignUser = (userId) => {
        axios.post(`/cases/${caseId}/assign-user/`, { user_id: userId }).then(() =>
            axios.get(`/cases/${caseId}/users/`).then((response) => setUsers(response.data))
        );
    };

    const removeUser = (userId) => {
        axios.post(`/cases/${caseId}/remove-user/`, { user_id: userId }).then(() =>
            axios.get(`/cases/${caseId}/users/`).then((response) => setUsers(response.data))
        );
    };

    return (
        <div className="container">
            <Sidebar />
            <div className="main-content">
                <div className="header">
                    <div>Case Number: {caseDetails.case_number}</div>
                    <div className="header-right">
                        <div>
                            Last Updated:{' '}
                            {caseDetails.last_updated &&
                                new Date(caseDetails.last_updated).toLocaleString()}
                        </div>
                    </div>
                </div>
                <CaseTabs caseId={caseId} activeTab="manage" />
                <div className="case-info">
                    <div>
                        Case First Opened:{' '}
                        {caseDetails.date_opened &&
                            new Date(caseDetails.date_opened).toLocaleDateString()}
                    </div>
                    <div>Case Owner: {caseDetails.created_by?.username}</div>
                    <div>Officers on Case: {users.length}</div>
                </div>
                <div className="content">
                    <div className="manage-case">
                        <div className="upload-documents" onClick={() => setIsFileUploadOpen(true)}>
                            Upload Documents
                        </div>
                        <div className="manage-files">Manage Files</div>
                    </div>
                    <div className="documents">
                        {documents.map((doc) => (
                            <div key={doc.file_id} className="document">
                                <a href={doc.file} target="_blank" rel="noopener noreferrer">
                                    {doc.file.split('/').pop()}
                                </a>
                            </div>
                        ))}
                    </div>
                    <div className="manage-users">
                        <h3>Manage Users</h3>
                        {users.map((user) => (
                            <div key={user.id} className="user">
                                {user.username}{' '}
                                <span className="remove" onClick={() => removeUser(user.id)}>
                                    Remove from case
                                </span>
                            </div>
                        ))}
                        <select onChange={(e) => assignUser(e.target.value)} defaultValue="">
                            <option value="" disabled>
                                + Assign another officer
                            </option>
                            {allUsers
                                .filter((user) => !users.find((u) => u.id === user.id))
                                .map((user) => (
                                    <option key={user.id} value={user.id}>
                                        {user.username}
                                    </option>
                                ))}
                        </select>
                    </div>
                </div>
            </div>
            {isFileUploadOpen && (
                <FileUpload
                    caseId={caseId}
                    onClose={() => setIsFileUploadOpen(false)}
                    onFileUploaded={() =>
                        axios.get(`/cases/${caseId}/files/`).then((response) =>
                            setDocuments(response.data)
                        )
                    }
                />
            )}
        </div>
    );
};

export default ManageCase;
