import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
// import 'regenerator-runtime/runtime';
import "../src/assets/style/frontpage_style.css"
import Dashboard from "./pages/Dashboard";
import Frontpage from "./pages/Frontpage";
import Login from "./pages/Login";
import Topic from "./pages/Topic";
import AssignmentsMCQ from "./pages/AssignmentsMCQ";
import AssignmentsFIB from "./pages/AssignmentsFIB";
import "./App.css";
import SelectYear from "./map/selectyear";
import Translator from "./pages/Translator";


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/tofrontpage" element={<Frontpage />} />
        <Route path="/todashboard" element={<Dashboard />} />
        <Route path="/topic/:courseName" element={<Topic />} />
        <Route path="/assignment/MCQ" element={<AssignmentsMCQ />} />
        <Route path="/assignment/Fill in the Blanks" element={<AssignmentsFIB />} />
        <Route path="/map" element={<SelectYear />} />
        <Route path="/translator" element={<Translator />} />
      </Routes>
    </Router>
  );
}

export default App;
