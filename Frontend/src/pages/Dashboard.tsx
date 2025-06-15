import React, { useEffect, useState, useContext, createContext } from 'react';
import { Link, useNavigate, useLocation } from "react-router-dom";
import "../assets/style/dashboard.css";
import { CircularProgressbar } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';
import APIService from '../api/APIService';

function Dashboard() {
  const navigate = useNavigate();
  const location = useLocation();


  const [username, setUsername] = useState(location.state?.username);
  const [exp_points, setExpPoints] = useState(location.state?.exp_points);
  const [progress, setProgress] = useState(0);

  // setUsername(location.state?.username);

  useEffect(() => {
    get_progress();

  }, []);

  function get_progress(){
    APIService.GetData('/dashboard').then((res:any) => {
      if(res.success){
        setExpPoints(res.exp_points);
        setProgress(parseInt(res.progress));
      }
    });
  }

  function toFrontpage() {
    APIService.GetData("/frontpage")
      .then((res:any) => {
        if (res) {
          navigate("/tofrontpage", { state: { username: location.state?.username, exp_points:res.leaderboard.exp_points } });
          // console.log(res);
          // console.log('dash->front');
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }



  function logout() {
    APIService.GetData('/logout').then((res:any)=>{
      if(res.success){
        localStorage.clear(); 
        window.location.href='/';
      }
    });
  }



  return (
    <>
<div className="container-fluid-custom">
  <div className="row-content-custom">
    

    <div className="col-custom-main">
      <div className="well-custom">
        <h4>Dashboard</h4>
        <div className="progress-bar-custom">
          {/* <div id="progress-custom">0%</div> */}
          <CircularProgressbar value={progress} text={`${progress}%`} />
        </div>  
      </div>
      <div className="row-custom">
        <div className="col-custom">
          <div className="well-custom">
            <h4>Welcome Back {location.state?.username}</h4> 
          </div>
        </div>
        <div className="col-custom">
          <div className="well-custom">
            <h4>Experience Points: {exp_points}</h4>
            {/* <p id="experience">{exp_points}</p>  */}
          </div>
        </div>
        <div className="col-custom">
          <div className="well-custom">
            <h4>Sessions</h4> 
          </div>
        </div>
      </div>
      <div className="row-custom">
        <div className="col-custom">
          <div className="well-custom">
            <p>Text</p> 
            <p>Text</p> 
            <p>Text</p> 
          </div>
        </div>
        <div className="col-custom">
          <div className="well-custom">
            <p>Text</p> 
            <p>Text</p> 
            <p>Text</p> 
          </div>
        </div>
        <div className="col-custom">
          <div className="well-custom">
            <p>Text</p> 
            <p>Text</p> 
            <p>Text</p> 
          </div>
        </div>
      </div>
      <div className="row-custom">
        <div className="col-custom">
          <div className="well-custom">
            <p>Text</p> 
          </div>
        </div>
        <div className="col-custom">
          <div className="well-custom">
            <p>Text</p> 
          </div>
        </div>
      </div>
    </div>

    <div className="col-custom-sidenav">
      <h2 style={{color: 'red'}}>Logo</h2>
      <ul className="nav-custom">
      {/* <a href="#"><li className="dash-btn">Dashboard</li></a> */}
      <a className="dash-btn" onClick={toFrontpage}><li>Front Page</li></a>
      <a className="dash-btn" onClick={logout}><li>Logout</li></a>
      </ul>
    </div>


  </div>
</div>



    </>
  );
}

export default Dashboard;
