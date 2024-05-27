export interface MessageModalParams {
  open: boolean;
  header?: string;
  message: string;
  acceptText?: string;
  cancelText?: string;
  onAccept?: () => void;
  onCancel?: () => void;
  type: 'accept' | 'cancel';
}


export function answerReducer(state: MessageModalParams, action: MessageAction): MessageModalParams {
  switch (action.type) {
    case 'show': {
      return {...action.params, open: true};
    }
    case 'close': {
      return {...state, open: false};
    }
    default: {
      throw Error('Unknown action');
    }
  }
}

export type MessageAction = 
  | {type: 'show', params: MessageModalParams}
  | {type: 'close'}