import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import FileUpload from './components/FileUpload';
import LoginPage from './pages/LoginPage';     // Updated path
import Dashboard from './pages/Dashboard';     // Updated path
import MyCases from './pages/MyCases';         // Updated path
import CaseDashboard from './pages/CaseDashboard';
import ManageCase from './pages/ManageCase';
import UpdatedCases from './pages/UpdatedCases';
import CaseChangeLog from './pages/CaseChangeLog';
import ReviewAnalysis from './pages/ReviewAnalysis';

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
                    <Route path="/updatedcases" element={<UpdatedCases />} />
                    <Route path="/case-dashboard/:caseId" element={<CaseDashboard />} />
                    <Route path="/case-change-log/:caseId" element={<CaseChangeLog />} />
                    <Route path="/review/:fileId" element={<ReviewAnalysis />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
