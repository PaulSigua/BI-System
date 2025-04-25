import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AboutComponent } from './about/about.component';
import { HomeComponent } from './home/home.component';
import { RouterModule, Routes } from '@angular/router';
import { LayoutsModule } from '../layouts/layouts.module';
import { ReportsComponent } from './reports/reports.component';
import { AuthGuard } from '../../guards/auth.guard';
import { HttpClientModule } from '@angular/common/http';

const routes: Routes = [
  {
    path: '',
    component: HomeComponent
  },
  {
    path: 'about',
    component: AboutComponent
  },
  {
    path: 'reports',
    component: ReportsComponent, 
    canActivate: [AuthGuard] 
  },
  {
    path: 'auth',
    loadChildren: () => import('../pages/auth/auth.module').then(m => m.AuthModule)
  }
];


@NgModule({
  declarations: [
    AboutComponent,
    HomeComponent,
    ReportsComponent,
  ],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    LayoutsModule,
    HttpClientModule
  ],
  exports: [
    AboutComponent,
    HomeComponent,
    RouterModule
  ]
})
export class PagesModule { }