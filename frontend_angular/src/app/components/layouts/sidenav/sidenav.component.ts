import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { ReportService } from '../../../services/report/report.service';
import { PowerBIReport } from '../../../models/models';
import { AuthService } from '../../../services/auth/auth.service';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
@Component({
  selector: 'app-sidenav',
  standalone: false,
  templateUrl: './sidenav.component.html',
  styleUrl: './sidenav.component.css'
})
export class SidenavComponent implements OnInit {

  @Input() reports: PowerBIReport[] = [];

  constructor(
    private reportService: ReportService,
    private authService: AuthService,
    private sanitizer: DomSanitizer,
  ) { }

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
    this.reportService.getReportByName(ownerId).subscribe({
      next: data => {
        this.reports = data;
        console.log('Reports loaded:', this.reports);
      },
      error: err => console.error('Error loading reports', err)
    });
  }

  getSafeUrl(url: string): SafeResourceUrl {
    return this.sanitizer.bypassSecurityTrustResourceUrl(url);
  }
}