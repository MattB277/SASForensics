import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from '../utils/axiosConfig'; // Make sure axiosConfig is set up for JWT
import '../styles/pages/LoginPage.css';

function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null); // For error message
  const navigate = useNavigate();

  const handleSignIn = async () => {
    console.log('Sign In Clicked', { username, password });

    try {
      // Make sure to call the correct login endpoint
      const response = await axios.post('/token/', {
        username,
        password,
      });

      // Assuming the backend returns 'access' and 'refresh' tokens
      const { access } = response.data; // Or whatever the correct token is called
      localStorage.setItem('authToken', access); // Store the access token
      navigate('/'); // Redirect to the home page or wherever you want after login
    } catch (err) {
      console.error('Login error:', err);
      setError('Invalid username or password.'); // Display error message to the user
    }
  };

  const handleSignUp = () => {
    navigate('/signup'); // Navigate to the signup page
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <h1>Cold Case Tracking System</h1>
        {error && <div className="error-message">{error}</div>} {/* Display error message */}
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="input-field"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="input-field"
        />
        <div className="button-container">
          <button onClick={handleSignIn} className="sign-in-button">
            Sign In
          </button>
          <button onClick={handleSignUp} className="sign-up-button">
            Sign Up
          </button>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;
