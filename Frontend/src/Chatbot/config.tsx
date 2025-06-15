import { createChatBotMessage } from 'react-chatbot-kit';
import DogPicture from './DogPicture';


const config = {
  initialMessages: [
    createChatBotMessage("Hello! What can I help you with today?", {})
  ],

  widgets: [
    {
      widgetName: 'dogPicture',
      widgetFunc: (props:any) => <DogPicture {...props} />,
      props: {},
      mapStateToProps: [],
    },
  ],
};

export default config;
