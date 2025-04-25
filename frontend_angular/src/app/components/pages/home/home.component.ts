import { Component } from '@angular/core';

@Component({
  selector: 'app-home',
  standalone: false,
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {

  pages = [
    { path: 'login', title: 'Iniciar Sesión' }
  ]
  constructor() { }

  
}
