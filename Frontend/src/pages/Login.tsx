import { useState } from "react";
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import APIService from "../api/APIService";
import '../App.css'

function Login () {
  const [authMode, setAuth] = useState("signin");
  const [msg, setMsg] = useState('');
  const navigate = useNavigate(); 
  const [student_name, setName] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');


  const changeAuthMode = () => {
    setAuth(authMode === "signin" ? "signup" : "signin")
  }

  const handleSubmit = (event:any) =>{

    event.preventDefault();

    if(authMode === "signin"){
      APIService.PostData({username:username, password:password}, '/login').then((res: any) => {

        
        if(res.success){
          APIService.GetData('/dashboard').then((res:any)=>{
            if(res.success){
              navigate('/todashboard', {state:{username:res.username, exp_points: res.exp_points}});
              // console.log('login->dash: ', res.username, res.exp_points);
            }
            else{
              console.log("Error in dashboard stuff");
              console.log('Res from dashboard', res);
            }
          });
          // navigate('/todashboard', {state:{student_name:res.name}});
          // console.log('RES: ', res);
        }
        else{
          console.log("Error in login ");
          console.log('RES: ', res);
        }

        
        
      });
    }
    else{
      APIService.PostData({student_name: student_name, username:username, password:password}, '/register').then((res: any) => {
        // navigate
        console.log(res);
        setMsg(res.msg)
        setAuth("signin");
      });
    }
  }



  if (authMode === "signin") {
    return (
      <div className="Auth-form-container">
        <form className="Auth-form" onSubmit={handleSubmit}>
          <div className="Auth-form-content">
            <h3 className="Auth-form-title">Sign In</h3>
            <div className="text-center">
              Not registered yet?{" "}
              <span className="change-link" onClick={changeAuthMode}>
                Sign Up
              </span>
            </div>
            <div className="form-group mt-3">
              <label>Enter Your Username</label>
              <input
                type="text"
                className="text-input"
                placeholder="Enter username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>
            <div className="form-group mt-3">
              <label>Password</label>
              <input
                type="password"
                className="text-input"
                placeholder="Enter password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
            <div className="submit-btn">
              <button type="submit" className="login-btn">
                Login
              </button>
            </div>
            <p className="text-center mt-2">
              {msg}
            </p>
          </div>
        </form>
      </div>
    )
  } else{

  return (
    <div className="Auth-form-container">
      <form className="Auth-form" onSubmit={handleSubmit}>
        <div className="Auth-form-content">
          <h3 className="Auth-form-title">Sign Up</h3>
          <div className="text-center">
            Already registered?{" "}
            <span className="change-link" onClick={changeAuthMode}>
              Sign In
            </span>
          </div>
          <div className="form-group mt-3">
            <label>Enter Name</label>
            <input
              type="text"
              className="text-input"
              placeholder="Enter Your Name"
              value={student_name}
              onChange={(e) => setName(e.target.value)}
            />
          </div>
          <div className="form-group mt-3">
            <label>Enter a Username</label>
            <input
              type="text"
              className="text-input"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>
          <div className="form-group mt-3">
            <label>Enter a Password</label>
            <input
              type="password"
              className="text-input"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <div className="submit-btn">
            <button type="submit" className="btn btn-primary">
              Sign Up
            </button>
          </div>
          {msg}
        </div>
      </form>
    </div>
  )}
};

export default Login;
