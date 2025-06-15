import React,{useState, useEffect} from "react";
import { Link, useParams, useNavigate, useLocation } from "react-router-dom";
import APIService from "../api/APIService";
import "../assets/style/topics.css";

interface Topic {
  name: string;
  video: string;
  description: string;
  topic_id: number;
}

function TopicPage() {
  const { courseName } = useParams<{ courseName: string }>();
  const assgn_type = ['MCQ', 'Fill in the Blanks'];
  const [topic, setTopic] = React.useState<Topic | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    lmao(courseName);
  }, [courseName]);

  console.log(courseName);

  const lmao = (courseName:any) => {
    APIService.PostData({}, `/topic/${courseName}`).then((res:any)=>{
      console.log(res);
      setTopic(res); 
    });
  }


  function checkAssignment(assgn_type: string) {

    APIService.PostData({courseName, assgn_type}, "/check-assignment").then((res: any) => {
      if (res.completed) {
        alert("Assignment Completed");
      }
      else{
        // APIService.GetData("complete-assignment").then((res:any)=>{

        // })

        navigate(`/assignment/${assgn_type}`, {state:{topic_name:courseName}});
      }

  })}



  const renderDescriptionList = (description: any) => {
    return (
        <div>
            {description.map((point: any, index: number) => (
                <div key={index}>{point}</div> 
            ))}
        </div>
        
    );
};


  return (
    <div className="container">
      {topic ? (
        <>
          <header>
            <h1>{topic.name}</h1>
            <a onClick={()=>navigate(-1)}>
              <button>Back to Front Page</button>
            </a>
          </header>

         <div className="page-content">
          <div className="page-content-child">
              <div className="video">
                <iframe
                  title="topic-video"
                  width="900"
                  height="540"
                  src={topic.video}
                  allowFullScreen
                ></iframe>
              </div>
            </div>
          
            <div className="page-content-child" id="assignments">
                <h2>Assignments</h2>
                <ul>
                  
                    <a onClick={() => checkAssignment(`${assgn_type[0]}`)} >
                      <li>Assignment 1: MCQ</li>
                    </a>
                  
                  
                    <a onClick={() => checkAssignment(`${assgn_type[1]}`)} >
                      <li>Assignment 2: Fill in the Blanks</li>
                    </a>
                  
                  
                    {/* <a onClick={() => checkAssignment(`${assgn_type[2]}`)}>
                      <li>Assignment 3: Match the Following</li>
                    </a> */}
                  
                </ul>
              </div>
          </div>
          <div className="desc">
            <h2>Description</h2>
            {renderDescriptionList(topic.description)}
         </div>
        </>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}

export default TopicPage;
