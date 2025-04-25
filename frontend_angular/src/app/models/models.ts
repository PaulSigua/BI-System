export interface PowerBIReport {
  ReportId: number;
  ReportName: string;
  ReportUrl: string;
  OwnerId: number;
  CreatedAt: string;
}

export interface User {
  UserId: number; 
  Username: string; 
  Email: string; 
  IsActive: boolean;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}