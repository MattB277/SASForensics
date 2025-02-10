import React from "react";
import '../../styles/components/Sidebar.css';
import logo from '../../assets/policelogo.png';
import { Link } from "react-router-dom";

function Sidebar() {
    const menuItems = [
        { path: "/", label: "Dashboard" },
        { path: "/mycases", label: "My Cases" },
        { path: "/updatedcases", label: "Updated Cases" },
        { path: "/login", label: "Login" },
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
            </div>
        </div>
    );
}

export default Sidebar;
