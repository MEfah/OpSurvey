export enum QuestionType {
  SingleSelect=0,
  SingleSelectOther=1,
  MultiSelect=2,
  MultiSelectOther=3,
  DropDown=4,
  InputText=5,
  InputNumber=6,
  InputInteger=7,
  InputDate=8,
  InputTime=9
}

export interface QuestionInfo {
  id: number;
  name: string;
  description?: string;
  questionType: QuestionType;
  shuffleOptions?: boolean;
  required: boolean;
  options?: QuestionOptionInfo[];
}

export interface QuestionOptionInfo {
  id: number;
  name: string;
}