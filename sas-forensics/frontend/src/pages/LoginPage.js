import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/pages/LoginPage.css';

function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSignIn = () => {
    console.log('Sign In Clicked', { username, password });
    navigate('/');
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <h1>Cold Case Tracking System</h1>
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
        <button onClick={handleSignIn} className="sign-in-button">
          Sign In
        </button>
        <button className="forgot-password-button">Forgot Password?</button>
      </div>
    </div>
  );
}

export default LoginPage;
