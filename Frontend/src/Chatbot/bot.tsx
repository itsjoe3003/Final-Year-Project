import React from 'react';
import { Chatbot } from 'react-chatbot-kit'; // Correct import statement with curly braces
import 'react-chatbot-kit/build/main.css';
import config from "./config.tsx";
import MessageParser from './MessageParser.js';
import ActionProvider from './ActionProvider.js';

import { Link, useNavigate, useLocation } from "react-router-dom";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

const CustomChatBot = () => { 

  const navigate = useNavigate();
  const location = useLocation();

  return (
    <>

        <header>
          <div className="user-info">
            <span id="username">Welcome back, {location.state?.username}!</span>
            {/* <span id="experience">Total Experience: {exp_points}</span> */}
          </div>
          {/* <a onClick={() => {navigate("/todashboard", {state:{username:location.state?.username}})}}> */}
          <a
            onClick={() => {
              navigate(-1);
            }}
          >
            <button id="dashboard-btn">Frontpage</button>
          </a>
          
        </header>


    <div>
        <Chatbot
        config={config}
        messageParser={MessageParser}
        actionProvider={ActionProvider}
      />
    </div>
    
    </>
    
  );
};

export default CustomChatBot;
