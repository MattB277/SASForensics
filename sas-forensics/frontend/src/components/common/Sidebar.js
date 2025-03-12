import React from "react";
import '../../styles/components/Sidebar.css';
import logo from '../../assets/policelogo.png';
import { Link, useNavigate } from "react-router-dom";

function Sidebar() {
    const isLoggedIn = !!localStorage.getItem('authToken');
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem('authToken');
        navigate('/login');
    };

    return (
        <div className="sidebar">
            <div className="logo">
                <img src={logo} alt="App Logo" className="logo-image" />
            </div>
            <div className="menu">
                <Link to="/" className="menu-button">Dashboard</Link>
                {isLoggedIn && <Link to="/account" className="menu-button">My Account</Link>}
                <Link to="/mycases" className="menu-button">My Cases</Link>
                <Link to="/updatedcases" className="menu-button">Updated Cases</Link>
                <Link to="/review-documents" className="menu-button">Review Analysis</Link>
                {isLoggedIn ? (
                    <button onClick={handleLogout} className="menu-button">Logout</button>
                ) : (
                    <Link to="/login" className="menu-button">Login</Link>
                )}
            </div>
        </div>
    );
}

export default Sidebar;