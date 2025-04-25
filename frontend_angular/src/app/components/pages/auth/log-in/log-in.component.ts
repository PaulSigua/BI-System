import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../../../services/auth/auth.service';

@Component({
  selector: 'app-log-in',
  standalone: false,
  templateUrl: './log-in.component.html',
  styleUrls: ['./log-in.component.css']
})
export class LogInComponent {
  credentials = { Username: '', PasswordHash: '' };
  error: string = '';

  constructor(private authService: AuthService, private router: Router) {}

  login() {
    this.authService.login(this.credentials).subscribe({
      next: () => {
        const user = JSON.parse(localStorage.getItem('user')!);
        const userReports = JSON.parse(localStorage.getItem('reports') || '[]')
          .filter((r: any) => r.OwnerId === user.UserId);
      
        if (userReports.length) {
          this.router.navigate(['report', userReports[0].ReportId]);
        } else {
          this.router.navigate(['report']);
        }
      },
      error: () => this.error = 'Credenciales inválidas'
    });
  }
}