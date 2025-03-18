import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import FileUpload from './components/FileUpload';
import LoginPage from './pages/LoginPage';     // Updated path
import Dashboard from './pages/Dashboard';     // Updated path
import MyCases from './pages/MyCases';         // Updated path
import MyAccount from './pages/MyAccount'; 
import CaseDashboard from './pages/CaseDashboard';
import ManageCase from './pages/ManageCase';
import UpdatedCases from './pages/UpdatedCases';
import CaseChangeLog from './pages/CaseChangeLog';
import CreateAccount from './pages/CreateAccount';
import ReviewAnalysis from './pages/ReviewAnalysis';
import ReviewDocuments from './pages/ReviewDocuments';
import DocumentDashboard from './pages/DocumentDashboard';
import CaseTimeline from './pages/CaseTimeline';
import DocumentChangeLog from './pages/DocumentChangeLog';
import DocumentAnalysis from './pages/DocumentAnalysis';
import CaseSummary from './pages/CaseSummary';

function App() {
    return (
        <Router>
            <div>

                {/* Routes */}
                <Routes>
                    <Route path="/" element={<Dashboard />} />
                    <Route path="/upload" element={<FileUpload />} />
                    <Route path="/manage-case/:caseId" element={<ManageCase />} />
                    <Route path="/login" element={<LoginPage />} />
                    <Route path="/dashboard" element={<Dashboard />} />
                    <Route path="/mycases" element={<MyCases />} />
                    <Route path="/account" element={<MyAccount />} />
                    <Route path="/updatedcases" element={<UpdatedCases />} />
                    <Route path="/case-dashboard/:caseId" element={<CaseDashboard />} />
                    <Route path="/case-summary/:caseId" element={<CaseSummary />} />
                    <Route path="/case-change-log/:caseId" element={<CaseChangeLog />} />
                    <Route path="/cases/:caseId/timeline" element={<CaseTimeline />} />
                    <Route path="/signup" element={<CreateAccount />} />
                    <Route path="/case/:caseId/document-dashboard/:fileId" element={<DocumentDashboard />} />
                    <Route path="/case/:caseId/document-change-log/:fileId" element={<DocumentChangeLog />} />
                    <Route path="/case/:caseId/document-analysis/:fileId" element={<DocumentAnalysis />} />
                    <Route path="/cases/:caseId/timeline" element={<CaseTimeline />} />
                    <Route path="/review/:fileId" element={<ReviewAnalysis />} />
                    <Route path="/review-documents" element={<ReviewDocuments />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
