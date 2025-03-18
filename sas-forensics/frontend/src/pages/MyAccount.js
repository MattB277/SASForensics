import React, { useState, useEffect } from 'react';
import axios from '../utils/axiosConfig'; // Assuming you have a preconfigured axios instance
import '../styles/pages/MyAccount.css';
import Sidebar from '../components/common/Sidebar';

const MyAccountPage = () => {
  const [userDetails, setUserDetails] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch the user's details when the component mounts
    const fetchUserDetails = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/user/info/', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          },
        });
        
        // Set user details once fetched
        setUserDetails(response.data);
      } catch (error) {
        // Handle the error (you can also add more detailed error handling)
        console.error('Error fetching user details:', error);
        setError('Failed to fetch user details. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchUserDetails();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    window.location.href = '/login';  // Redirect to login page
  };

  if (loading) {
    return <div className="loading-spinner">Loading...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  return (
    <div className="dashboard-container">
      {/* Sidebar */}
      <Sidebar />

      {/* Content Section */}
      <div className="dashboard-content">
        <h1>My Account</h1>
        <div className="user-details">
          <p><strong>Username:</strong> {userDetails.username}</p>
          <p><strong>Email:</strong> {userDetails.email}</p>
          {/* You can display other user details here as needed */}
        </div>
      </div>
    </div>
  );
};

export default MyAccountPage;
