import React from 'react';
import { createContext, useContext} from 'react';
import { MessageModalParams } from '../../reducers/MessageReducer';


const MessagesContext = createContext<MessageModalParams | null>(null);


const MessagesDispatchContext = createContext<React.Dispatch<MessageModalParams> | null>(null);


export function useMessages() {
  return useContext(MessagesContext);
}


export function useMessagesDispatch() {
  return useContext(MessagesDispatchContext);
}


interface AnswerProviderProps {
  children: React.ReactNode;
  answer: MessageModalParams;
  dispatch: React.Dispatch<MessageModalParams>;
}


export function MessageProvider(props: AnswerProviderProps) {
  return (
    <MessagesContext.Provider value={props.answer}>
      <MessagesDispatchContext.Provider value={props.dispatch}>
        {props.children}
      </MessagesDispatchContext.Provider>
    </MessagesContext.Provider>
  );
}