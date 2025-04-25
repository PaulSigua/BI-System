import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LogInComponent } from './log-in/log-in.component';
import { RegisterComponent } from './register/register.component';
import { RouterModule, Routes } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { LayoutsModule } from '../../layouts/layouts.module';
import { AuthGuard } from '../../../guards/auth.guard';

const routes: Routes = [
  { 
    path: 'login',
    component: LogInComponent
  },
  { 
    path:'register', 
    component: RegisterComponent
  }
];

@NgModule({
  declarations: [
    LogInComponent,
    RegisterComponent
  ],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    FormsModule,
    LayoutsModule
  ]
})
export class AuthModule { }