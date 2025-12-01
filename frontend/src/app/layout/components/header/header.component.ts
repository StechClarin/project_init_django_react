import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

// ✅ On utilise l'alias @core pour l'import propre
import { AuthService } from '@core/services/auth.service';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule],
  template: `
    <header class="fixed top-0 right-0 left-64 h-16 bg-white shadow-sm border-b border-gray-200 flex items-center justify-between px-6 z-40 transition-all duration-300">
      
      <div class="flex items-center">
        <h1 class="text-xl font-semibold text-gray-800 tracking-tight">
          Administration
        </h1>
      </div>

      <div class="flex items-center space-x-4">
        
        <button class="p-2 text-gray-400 hover:text-indigo-600 transition-colors relative">
          <span class="absolute top-2 right-2 h-2 w-2 rounded-full bg-red-500 ring-2 ring-white"></span>
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path></svg>
        </button>

        <div class="h-8 w-px bg-gray-200 mx-2"></div>

        <div class="flex items-center gap-3 cursor-pointer group">
          <div class="text-right hidden sm:block">
            <p class="text-sm font-medium text-gray-900 group-hover:text-indigo-600 transition-colors">
              EtherNanos
            </p>
            <p class="text-xs text-gray-500">Super Admin</p>
          </div>

          <div class="h-10 w-10 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold shadow-md border-2 border-white">
            E
          </div>
        </div>

        <button 
          (click)="logout()" 
          class="ml-2 p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-full transition-all" 
          title="Se déconnecter">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>
        </button>
      </div>

    </header>
  `
})
export class HeaderComponent {
  private authService = inject(AuthService);
  
  // Pas besoin d'injecter Router ici, car le AuthService gère la redirection dans logout()
  // Mais on peut le garder si on veut faire une redirection spécifique.

  logout() {
    this.authService.logout();
  }
}