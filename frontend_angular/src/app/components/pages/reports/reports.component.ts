import { Component } from '@angular/core';
import { PowerBIReport } from '../../../models/models';
import { ReportService } from '../../../services/report/report.service';
import { AuthService } from '../../../services/auth/auth.service';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';

@Component({
  selector: 'app-reports',
  standalone: false,
  templateUrl: './reports.component.html',
  styleUrl: './reports.component.css'
})
export class ReportsComponent {

  reports: PowerBIReport[] = [];

  constructor(
    private reportService: ReportService,
    private authService: AuthService,
    private sanitizer: DomSanitizer
  ) {}

  ngOnInit() {
    const user = this.authService.getCurrentUser();
    if (user?.UserId) {
      this.loadReports(user.UserId);
    } else {
      this.authService.currentUser$.subscribe(u => {
        if (u?.UserId) {
          this.loadReports(u.UserId);
        }
      });
    }
  }

  private loadReports(ownerId: number) {
    this.reportService.getReportsByOwner(ownerId).subscribe({
      next: data => {
        this.reports = data;
        console.log('Reports loaded:', this.reports); // <-- dentro del subscribe
      },
      error: err => console.error('Error loading reports', err)
    });
  }

  getSafeUrl(url: string): SafeResourceUrl {
    return this.sanitizer.bypassSecurityTrustResourceUrl(url);
  }
  
}
