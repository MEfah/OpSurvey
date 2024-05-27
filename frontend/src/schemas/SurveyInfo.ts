export default interface SurveyInfo {
  id: string;
  name: string;
  creatorId: string;
  creatorName: string;
  creatorImgSrc?: string;
  description?: string;
  imgSrc?: string;
  completionCount: number;
  completionTime: number;
  questionCount: number;
  requiredCount: number;
  creationDate: Date;
}