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

    // Static menu items that always appear
    const menuItems = [
        { path: "/", label: "Dashboard" },
        { path: "/mycases", label: "My Cases" },
        { path: "/updatedcases", label: "Updated Cases" },
        { path: "/review-documents", label: "Review Analysis"}
    ];

    return (
        <div className="sidebar">
            <div className="logo">
                <img src={logo} alt="App Logo" className="logo-image" />
            </div>
            <div className="menu">
                {menuItems.map((item, index) => (
                    <Link key={index} to={item.path} className="menu-button">
                        {item.label}
                    </Link>
                ))}
                {isLoggedIn ? (
                    <>
                        <Link to="/account" className="menu-button">My Account</Link>
                        <button onClick={handleLogout} className="menu-button">Logout</button>
                    </>
                ) : (
                    <Link to="/login" className="menu-button">Login</Link>
                )}
            </div>
        </div>
    );
}

export default Sidebar;
