import { Component } from '@angular/core';
import { PowerBIReport } from '../../../models/models';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-report-detail',
  standalone: false,
  templateUrl: './report-detail.component.html',
  styleUrl: './report-detail.component.css'
})
export class ReportDetailComponent {
  reports: PowerBIReport[] = [];
  reportId!: number;
  report?: PowerBIReport;
  safeUrl?: SafeResourceUrl;

  constructor(
    private route: ActivatedRoute,
    private sanitizer: DomSanitizer
  ) {}

  ngOnInit(): void {
    this.reportId = +this.route.snapshot.paramMap.get('id')!;
    
    // Simulación: puedes reemplazar esto con una llamada a tu servicio real
    const allReports = JSON.parse(localStorage.getItem('reports') || '[]');
    console.log('Reportes: ', allReports)
    this.report = allReports.find((r: PowerBIReport) => r.ReportId === this.reportId);

    if (this.report) {
      this.safeUrl = this.sanitizer.bypassSecurityTrustResourceUrl(this.report.ReportUrl);
    }
  }

  getSafeUrl(url: string): SafeResourceUrl {
    return this.sanitizer.bypassSecurityTrustResourceUrl(url);
  }
}
