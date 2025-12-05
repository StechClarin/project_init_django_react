import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { CommonModule } from '@angular/common'; // Added CommonModule

// On utilise les alias pour importer les briques
import { SidebarComponent } from '../components/sidebar/sidebar.component'; // Path changed
import { HeaderComponent } from '../components/header/header.component'; // Path changed
import { UiToastComponent } from '@shared/components/ui-toast/ui-toast.component'; // Added UiToastComponent

@Component({
  selector: 'app-main-layout',
  standalone: true,
  // On importe les 3 éléments nécessaires pour la page
  imports: [CommonModule, RouterOutlet, SidebarComponent, HeaderComponent, UiToastComponent], // Added CommonModule and UiToastComponent
  template: `
    <div class="flex h-screen bg-slate-50 overflow-hidden">
      <app-ui-toast></app-ui-toast>
      
      <!-- Sidebar -->
      <app-sidebar></app-sidebar>

      <div class="pl-72 flex flex-col min-h-screen transition-all duration-300">
        
        <app-header></app-header>

        <main class="flex-1 pt-24 px-8 pb-8 overflow-x-hidden">
          <div class="max-w-7xl mx-auto">
            <router-outlet></router-outlet>
          </div>
        </main>

      </div>
    </div>
  `
})
export class MainLayoutComponent { }