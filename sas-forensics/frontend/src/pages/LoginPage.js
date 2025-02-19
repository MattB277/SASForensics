import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from '../utils/axiosConfig'; 
import '../styles/pages/LoginPage.css';

function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null); 
  const navigate = useNavigate();

  const handleSignIn = async () => {
    console.log('Sign In Clicked', { username, password });
    try {
      const response = await axios.post('/login/', {
        username,
        password,
      });

      const { token } = response.data;
      localStorage.setItem('token', token); 
      navigate('/'); 
    } catch (err) {
      console.error('Login error:', err);
      setError('Invalid username or password.'); 
    }
  };

  const handleSignUp = () => {
    navigate('/signup')};

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
