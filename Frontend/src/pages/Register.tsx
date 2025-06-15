import { useState } from "react";
import "./assets/style/login_style.css";
import "./assets/style/styles.css";
import axios from 'axios';

const Register: React.FC = () => {
  const [studentname, setStudentname] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [msg, setMsg] = useState('');

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    
    try {
      const response = await fetch('/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ studentname, username, password })
      });

      const data = await response.json();

      if (response.ok) {
        // Registration successful, redirect to login page
        window.location.href = '/login';
      } else {
        // Registration failed, display error message
        setMsg(data.msg);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="login">
      <h1>Register</h1>
      <div className="links">
        <a href="{ url_for('login') }" className="active">Login</a>
        <a href="{ url_for('register') }">Register</a>
      </div>
      <form onSubmit={handleSubmit}>
        <label htmlFor="studentname">
          <i className="fas fa-profile"></i>
        </label>
        <input type="text" name="studentname" placeholder="Name" id="studentname" required value={studentname} onChange={(e) => setStudentname(e.target.value)} />
        <label htmlFor="username">
          <i className="fas fa-user"></i>
        </label>
        <input type="text" name="username" placeholder="Username" id="username" required value={username} onChange={(e) => setUsername(e.target.value)} />
        <label htmlFor="password">
          <i className="fas fa-lock"></i>
        </label>
        <input type="password" name="password" placeholder="Password" id="password" required value={password} onChange={(e) => setPassword(e.target.value)} />
        <div className="msg">{msg}</div>
        <input type="submit" value="Register" />
      </form>
    </div>
  );
};

export default Register;
