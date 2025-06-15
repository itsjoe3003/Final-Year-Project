import React, { useState, useEffect } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import APIService from "../api/APIService";
import { arr } from "./courses.tsx";
import ProgressBar from "@ramonak/react-progress-bar";
import "../assets/style/frontpage_style.css"


import { Chatbot } from 'react-chatbot-kit'; // Correct import statement with curly braces
import 'react-chatbot-kit/build/main.css';
import config from "../Chatbot/config.tsx";
import MessageParser from '../Chatbot/MessageParser.js';
import ActionProvider from '../Chatbot/ActionProvider.js';



function Frontpage() {
  const navigate = useNavigate();
  const location = useLocation();

  const [id, setID] = useState<string>("");
  const [name, setName] = useState<string>(location.state.username);
  const [leaderboardData, setLeaderboardData] = useState([]);
  const [exp_points, setExpPoints] = useState(location.state?.exp_points);
  const [progress, setProgress] = useState(0);
  const [showChatbot, setShowChatbot] = useState<boolean>(false);

  useEffect(() => {
    fetchLeaderboardData();
    // get_progress();
  }, []);

  function get_progress() {
    APIService.GetData("/dashboard").then((res: any) => {
      if (res) {
        setExpPoints(res.exp_points);
        setProgress(parseInt(res.progress));
      }
    });
  }

  const fetchLeaderboardData = () => {
    APIService.GetData("/frontpage")
      .then((res: any) => {
        if (res) {
          console.log(res);
          setLeaderboardData(res.leaderboard.leaderboard);
          get_progress();
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };




  return (
    <>
      <div>
        <header>
          <div className="user-info">
            <span id="username">Welcome back, {location.state?.username}!</span>
            <span id="experience">Total Experience: {exp_points}</span>
          </div>

      
          <div className="front-btns">
          <a onClick={() => {navigate(-1);}}>
            <button id="dashboard-btn">Dashboard</button>
          </a>
          
          
          <a onClick={()=>{navigate("/translator", {state:{username:location.state?.username}})}}>
            <button id="dashboard-btn">Speak and Learn</button>
          </a>


          <a href="/src/map/SelectYear.html">
            <button id="back-btn">Map</button>
          </a>
          </div>
        </header>

        <div id="progress-bar">
          {/* <div id="progress">0%</div> */}
          <ProgressBar completed={progress} />
        </div>

        <div className="container">

        <div className="leaderboard">
            <h2>Leaderboard</h2>
            <div id="leaderboard-list">
              <table>
                <thead>
                  <tr>
                    <th> Rank </th>
                    <th> Student Name </th>
                    <th> Total Score </th>
                  </tr>
                </thead>
                <tbody>
                  {leaderboardData ? (
                    leaderboardData.map((item: any, index) => (
                      <tr key={index}>
                        <td>{index + 1}</td>
                        <td>{item.student_name}</td>
                        <td>{item.marks}</td>
                      </tr>
                    ))
                  ) : (
                    <p>Loading...</p>
                  )}
                </tbody>
              </table>
            </div>
          </div>

        <div className="courses">
            <h2>Courses</h2>
            {arr.map((item, index) => {
              return (
                <div className="course" key={index}>
                  <h3>{item.Title}</h3>
                  <p>{item.content}</p>
                  <Link to={`/topic/${item.Title}`}>Learn More</Link>
                </div>
              );
            })}
          </div>



          

          
        </div>
      </div>

      <div>
      
      
    </div>
    </>
  );
}

export default Frontpage;
