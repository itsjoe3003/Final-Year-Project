import React from 'react';

interface MessageParserProps {
  children: React.ReactNode;
  actions?: any; 
}

const MessageParser: React.FC<MessageParserProps> = ({ children, actions }) => {
  const parse = (message: any) => {
    if(message != 'dog')
      actions.handleMessage(message);
    else
      actions.handleDog();
  };

  return (
    <div>
      {React.Children.map(children, (child) => {
        return React.cloneElement(child as React.ReactElement<any>, {
          parse: parse,
          actions: {},
        });
      })}
    </div>
  );
};


export default MessageParser;
