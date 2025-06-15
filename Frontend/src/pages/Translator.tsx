import React from 'react';
import { Link, useNavigate, useLocation } from "react-router-dom";
import { useState, useEffect } from 'react';
import APIService from "../api/APIService";
import SpeechRecognition, { useSpeechRecognition } from "react-speech-recognition";
// import { useSpeechSynthesis } from 'react-speech-kit';

import {
  MinChatUiProvider,
  MainContainer,
  MessageInput,
  MessageContainer,
  MessageList,
  MessageHeader
} from "@minchat/react-chat-ui";
import "../assets/style/translator.css";


interface Message {
  text: string;
  user: {
      id: string;
      name: string;
  };
  isServer: boolean; 
}


const Translator = () => {


  const navigate = useNavigate();
  const [messages, setMessages] = useState<Message[]>([
    {
        text: 'Hi, what can I translate for you today?',
        user: {
            id: 'server',
            name: 'Translator',
        },
        isServer: true, 
    },
]);

const {
  transcript,
  interimTranscript,
  finalTranscript,
  resetTranscript,
  listening,
} = useSpeechRecognition();

// useEffect(() => {
//   console.log('Transcript:', transcript);
//   console.log('Interim Transcript:', interimTranscript);
//   console.log('Final Transcript:', finalTranscript);
// }, [transcript, interimTranscript, finalTranscript]);


const speakText = (text:string) => {
  const synthesis = window.speechSynthesis;
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = 'ta-IN'; 
  synthesis.speak(utterance);
};

  


  const handleOnSendMessage = (text: string) => {
    console.log('in handle: '+ text);

    const userMessage: Message = {
        text,
        user: {
            id: 'user1',
            name: 'User',
        },
        isServer: false, 
    };

    setMessages((prevMessages) => [...prevMessages, userMessage]);

    
    APIService.PostData({text}, '/chatbot').then((res:any)=>{
      console.log(res);

        const serverResponse: Message = {
            text: res,
            user: {
                id: 'server',
                name: 'Translator',
            },
            isServer: true, 
        };
        setMessages((prevMessages) => [...prevMessages, serverResponse]);
        // speakText('another one');    
        speakText(res);
      
    });
    
    
};
 



  if (!SpeechRecognition.browserSupportsSpeechRecognition()) {
    return null;
  }
 
  if (!SpeechRecognition.browserSupportsSpeechRecognition()) {
    console.log('Try chrome browser');
  }

  const listenContinuously = () => {
    SpeechRecognition.startListening({
      continuous: true,
      language: 'en-US',
    });
  };

  // const handleStop = () =>{
  //   SpeechRecognition.stopListening(); 
  //   handleOnSendMessage(transcript); 
  //   resetTranscript();
  // }


  return(
    <>

  <header className="back-btn">
      <h1>Chat and Learn</h1>
      <a onClick={() => navigate(-1)}>
          <button id="dashboard-btn">Front Page</button>
      </a>
  </header>

      <div className="main-container">
      <div className="mic">
      <p>Microphone: {listening ? 'on' : 'off'}</p>
      <button onClick={()=>{resetTranscript(); listenContinuously();}}>Start</button>
      <a onClick={()=>{SpeechRecognition.stopListening(); handleOnSendMessage(transcript); resetTranscript(); }}><button> Stop</button></a>
      {/* <a onClick={()=>{handleStop}}><button> Stop</button></a> */}
      {/* <button onClick={()=>speakText(finalTranscript)}>Reset</button> */}
      <p></p>
      </div>



      <div className="chat-container" style={{ display: 'flex', justifyContent: 'center', padding: '20px' }}>
                <MinChatUiProvider theme="#6ea9d7">
                    <MainContainer style={{ height: '80vh', width: '80vw' }}>
                        <MessageContainer>
                            <MessageHeader />
                            <MessageList
                                currentUserId="user1"
                                messages={messages} />
                            <MessageInput
                                placeholder="Type message here"
                                onSendMessage={handleOnSendMessage}
                                showSendButton={true}
                                showAttachButton={false}
                            />
                        </MessageContainer>
                    </MainContainer>
                </MinChatUiProvider>
        </div>
      </div>
      

    </>
  );
};



export default Translator;