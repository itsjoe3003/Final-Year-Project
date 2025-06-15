import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import APIService from "../api/APIService";
import { fib_questions } from "./fib_questions";
import '../assets/style/mcq_style.css'
// import { Draggable, Droppable } from "../../node_modules/react-drag-and-drop";


function AssignmentsFIB() {
  const navigate = useNavigate();
  const location = useLocation();
  const initialTopicName: string = location.state?.topic_name || "";
  const [marks, setMarks] = useState<number>(0);
  var [temp_qs, setQuestions] = useState<{ question: string; options: string[]; answer: string; selectedAns: string; }[]>(fib_questions[initialTopicName as keyof typeof fib_questions] as { question: string; options: string[]; answer: string; selectedAns: string; }[]);


  useEffect(() => {
    const selectedQuestions = fib_questions[initialTopicName as keyof typeof fib_questions] as { question: string; options: string[]; answer: string; selectedAns: string; }[];
    if (selectedQuestions) {
      setQuestions(selectedQuestions);
    }
  }, [initialTopicName]);
  

  const handleChange = (questionIndex: number, selectedOption: string) => {
    const updatedQuestions = [...temp_qs];
    updatedQuestions[questionIndex] = {
      ...updatedQuestions[questionIndex],
      selectedAns: selectedOption
    };
    setQuestions(updatedQuestions);
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const totalMarks = calculateTotalMarks();
    setMarks(totalMarks);
    completeAssignment(event, totalMarks);
  };

  const calculateTotalMarks = (): number => {
    let totalMarks = 0;
    temp_qs.forEach((question) => {
      if (question.selectedAns === question.answer) {
        totalMarks += 1;
      }
    });
    return totalMarks;
  };

  const completeAssignment = (event: React.FormEvent<HTMLFormElement>, marks: number) => {
    event.preventDefault();
    APIService.PostData(
      { topic_name: location?.state.topic_name, marks: marks, assignment_name: "Fill in the Blanks" },
      "/complete-assignment"
    ).then((res: any) => {
      console.log(res);
    });
  };


  return (
    <div className="fib_container">
       <div>
        <header className="mcq_header">
          <h2>Assignment: {location?.state.topic_name}</h2>
          <button onClick={() => navigate(-1)}>Go Back</button>
        </header>
        <div className="temp">
          <form id="assignmentForm" onSubmit={handleSubmit}>
            {temp_qs.map((item, index) => (
              <div className="question" key={index}>
                <h3>{item.question}</h3>
                {item.options.map((option, optionIndex) => (
                  <div className="radio-item">
                  <label key={optionIndex}>
                    <input
                      className ="radio-button"
                      type="radio"
                      name={`q${index + 1}`}
                      value={String.fromCharCode(optionIndex + 65)}
                      onChange={() => handleChange(index, String.fromCharCode(optionIndex + 65))}
                    />
                    {option}
                    <br />
                  </label>
                  </div>
                ))}
              </div>
            ))}
            <button type="submit">Submit</button>
          </form>
        </div>
        <p>Total Marks: {marks}</p>
        {/* <h3 onClick={testing}>Click</h3> */}
      </div>
    </div>
  );
}

export default AssignmentsFIB;