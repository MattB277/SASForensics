import React, { useState } from 'react'; 
import { useNavigate } from 'react-router-dom';
import axios from '../utils/axiosConfig';
import '../styles/pages/SignUpPage.css';
import logo from '../assets/policelogo.png';

export default function SignUp() {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      const response = await axios.post('/signup/', {
        first_name: firstName,
        last_name: lastName,
        username,
        password
      });

      if (response.status === 201) { 
        navigate("/login");
      } else {
        const data = response.data;
        setError(data.error || "Sign-up failed");
      }
    } catch (err) {
      console.error('Signup error:', err.response?.data || err.message);
      setError(err.response?.data?.error || "Network error");
    }
  };

  return (
    <div className="signup-page">
      <div className="signup-container">
        <img src={logo} alt="App Logo" className="signup-logo" />
        <h1>Cold Case Tracking System</h1>
        {error && <p className="error-message">{error}</p>}
        <form onSubmit={handleSubmit} className="form-container">
          <input
            type="text"
            placeholder="First Name"
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
            className="input-field"
          />
          <input
            type="text"
            placeholder="Last Name"
            value={lastName}
            onChange={(e) => setLastName(e.target.value)}
            className="input-field"
          />
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
          <button type="submit" className="sign-up-button">
            Sign Up
          </button>
        </form>
      </div>
    </div>
  );
}