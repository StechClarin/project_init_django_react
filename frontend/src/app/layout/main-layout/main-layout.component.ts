import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

// On utilise les alias pour importer les briques
import { SidebarComponent } from '@layout/components/sidebar/sidebar.component';
import { HeaderComponent } from '@layout/components/header/header.component';

@Component({
  selector: 'app-main-layout',
  standalone: true,
  // On importe les 3 éléments nécessaires pour la page
  imports: [RouterOutlet, SidebarComponent, HeaderComponent],
  template: `
    <div class="min-h-screen bg-gray-50">
      
      <app-sidebar></app-sidebar>

      <div class="pl-64 flex flex-col min-h-screen">
        
        <app-header></app-header>

        <main class="flex-1 pt-16 p-6 overflow-x-hidden">
          <div class="max-w-7xl mx-auto">
            <router-outlet></router-outlet>
          </div>
        </main>

      </div>
    </div>
  `
})
export class MainLayoutComponent {}