import React from 'react';
import APIService from '../api/APIService';
import { createChatBotMessage } from 'react-chatbot-kit'; // Import the function from the library

interface ActionProviderProps {
  createChatBotMessage: Function; // Specify the type for createChatBotMessage
  setState: Function; // You can specify the type for setState as needed
  children: React.ReactNode; // Specify the type for children
}

const ActionProvider: React.FC<ActionProviderProps> = ({ createChatBotMessage, setState, children }) => {


  const handleMessage = (mssg:any) =>{
    APIService.PostData({mssg:mssg}, '/chatbot').then((res: any) => {
      const newMessage = createChatBotMessage(res);
      console.log(res);
      setState((prev:any) => ({
        ...prev,
        messages: [...prev.messages, newMessage],
      }));
    });
  }


  const handleOptionsAction = (option: string) => {

    const response = `You selected ${option}.`; 
    const newMessage = createChatBotMessage(response);
    setState((prev:any) => ({
      ...prev,
      messages: [...prev.messages, newMessage],
    }));
  };

  const handleDog = () => {
    const botMessage = createChatBotMessage(
      "Here's a nice dog picture for you!",
      {
        widget: 'dogPicture',
      }
    );

    setState((prev:any) => ({
      ...prev,
      messages: [...prev.messages, botMessage],
    }));
  };


  return (
    <div>
      {React.Children.map(children, (child) => {
        return React.cloneElement(child as React.ReactElement<any>, {
          actions: {handleMessage, handleDog},
        });
      })}
    </div>
  );
};

export default ActionProvider;
