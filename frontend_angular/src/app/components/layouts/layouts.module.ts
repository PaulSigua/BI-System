import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FooterComponent } from './footer/footer.component';
import { SidenavComponent } from './sidenav/sidenav.component';
import { RouterModule } from '@angular/router';
import { HeaderComponent } from './header/header.component';
import { LucideAngularModule, Facebook, Twitter, Instagram, Linkedin } from 'lucide-angular';
import { FormsModule } from '@angular/forms';



@NgModule({
  declarations: [
    FooterComponent,
    SidenavComponent,
    HeaderComponent
  ],
  imports: [
    CommonModule,
    RouterModule,
    LucideAngularModule.pick({ Facebook, Twitter, Instagram, Linkedin }),
    FormsModule

  ],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  exports: [
    FooterComponent,
    SidenavComponent,
    HeaderComponent
  ]
})
export class LayoutsModule { }