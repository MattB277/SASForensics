import React, { useState, useEffect } from 'react';
import axios from '../utils/axiosConfig'; // Assuming you have a preconfigured axios instance

const MyAccountPage = () => {
  const [userDetails, setUserDetails] = useState(null);
  const [error, setError] = useState(null);

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
      }
    };

    fetchUserDetails();
  }, []);

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  if (!userDetails) {
    return <div>Loading user details...</div>;
  }

  return (
    <div className="my-account-container">
      <h1>My Account</h1>
      <div className="user-details">
        <p><strong>Username:</strong> {userDetails.username}</p>
        <p><strong>Email:</strong> {userDetails.email}</p>
        {/* You can display other user details here as needed */}
      </div>
    </div>
  );
};

export default MyAccountPage;
