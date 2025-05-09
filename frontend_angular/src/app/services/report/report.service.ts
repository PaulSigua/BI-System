import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from '../auth/auth.service';
import { AssignRole, PowerBIReport } from '../../models/models';

@Injectable({
  providedIn: 'root'
})
export class ReportService {
  private baseUrl = 'http://localhost:9999/api';

  constructor(
    private http: HttpClient,
    private auth: AuthService
  ) {}

  private headers(): HttpHeaders {
    const token = this.auth.getToken();
    return new HttpHeaders().set('Authorization', `Bearer ${token}`);
  }

  getReportsByOwner(ownerId: number): Observable<PowerBIReport[]> {
    return this.http.get<PowerBIReport[]>(`${this.baseUrl}/reports/owner/${ownerId}`, { headers: this.headers() });
  }

  getReportByName(ownerId: number): Observable<PowerBIReport[]> {
    return this.http.get<PowerBIReport[]>(`${this.baseUrl}/reports/name/${ownerId}`, { headers: this.headers() });
  }

  getRolByUser(userId: number): Observable<AssignRole[]> {
    return this.http.get<AssignRole[]>(`${this.baseUrl}/reports/name/${userId}`, { headers: this.headers() });
  }
}
