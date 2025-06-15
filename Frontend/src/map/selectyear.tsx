import React,{useState, useEffect} from "react";
import { Link, useParams, useNavigate, useLocation } from "react-router-dom";
// import "./style.css";


function SelectYear() {

  const navigate = useNavigate();

  const containerStyle: React.CSSProperties = {
    maxWidth: "800px",
    margin: "20px auto",
    display: "grid",
    gridTemplateColumns: "repeat(auto-fill, minmax(150px, 1fr))",
    gridGap: "20px",
    padding: "20px",
    color: "black",
  };

  const gridItemStyle: React.CSSProperties = {
    backgroundColor: "#ffffff",
    border: "1px solid #ccc",
    padding: "20px",
    textAlign: "center",
    cursor: "pointer"
  };

  

  const gridItemHoverStyle: React.CSSProperties = {
    backgroundColor: "#a4ecbe"
  };

  return (
    <>
      {/* <h1>Select an Era to Learn more about the Events that took place</h1>  */}
      <header>
            <h1>Select An Era</h1>
            <a onClick={()=>navigate(-1)}>
              <button>Back to Front Page</button>
            </a>
      </header>
      <div className="container" style={{ maxWidth: "800px",
    margin: "20px auto",
    display: "grid",
    gridTemplateColumns: "repeat(auto-fill, minmax(150px, 1fr))",
    gap: "20px",
    padding: "20px",}}>
        <a href="/src/map/200_BCE_200_CE.html" style={gridItemStyle}> BCE - 200 CE </a>
        <a href="/src/map/130.html" style={gridItemStyle}> 130</a>
        <a href="/src/map/190.html" style={gridItemStyle}> 190</a>
        <a href="/src/map/210.html" style={gridItemStyle}> 210</a>
        <a href="/src/map/300-590.html" style={gridItemStyle}> 300 - 590</a>
        <a href="/src/map/560-580.html" style={gridItemStyle}> 560 - 580</a>
        <a href="/src/map/590-630.html" style={gridItemStyle}> 590 - 630</a>
        <a href="/src/map/628.html" style={gridItemStyle}> 628 </a>
        <a href="/src/map/670-700.html" style={gridItemStyle}> 670 - 700</a>
        <a href="/src/map/800-830.html" style={gridItemStyle}> 800 - 830</a>
        <a href="/src/map/848.html" style={gridItemStyle}> 848</a>
        <a href="/src/map/903.html" style={gridItemStyle}> 903</a>
        <a href="/src/map/1023.html" style={gridItemStyle}> 1023</a>
        <a href="/src/map/1246.html" style={gridItemStyle}> 1246</a>
        <a href="/src/map/1279.html" style={gridItemStyle}> 1279</a>
        <a href="/src/map/1308.html" style={gridItemStyle}> 1308</a>
        <a href="/src/map/1522.html" style={gridItemStyle}> 1522</a>
        <a href="/src/map/1609.html" style={gridItemStyle}> 1609</a>
      </div>
    </>
  );
}

export default SelectYear;
